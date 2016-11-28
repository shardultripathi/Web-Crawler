import sys
import urllib2
import urlparse
import json
from bs4 import BeautifulSoup

Crawled = set()   # keeps a check of already visited web pages
pages = []

"""Handling proxy"""
proxy_support = urllib2.ProxyHandler({}) # change proxy settings like below if need be
# proxy_support = urllib2.ProxyHandler({"http":"http://a.b.c.d:port","https":"http://q.r.s.t:port"}) # example
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

def set_default(obj):
    """convert set to serializable list"""
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

class Page():
    """Page url and static assets"""
    def __init__(self, url, assets):
        self.url = url
        self.assets = assets

    def dump(self):
        return {'url': self.url,'assets': self.assets}

def findUrlsAssets (tag, attribute, soup, list):
    """Adds the tag attribute to list"""
    tags = soup.findAll(tag)
    for x in tags:
        try:
            list.append(x[attribute])
        except KeyError as e:
            pass

def startCrawling(seed, d, limit):
    print "Crawling:",seed
    try:
        conn = urllib2.urlopen(seed)    # establish connection to the url
        Crawled.add(seed)
    except:
        print "Error connecting to", seed
        return

    html = conn.read()  # get html source
    soup = BeautifulSoup(html, "html.parser")
    assets = []
    urls = []
    findUrlsAssets("a","href",soup,urls)   #url
    findUrlsAssets("iframe","src",soup,urls)  #url
    findUrlsAssets("img","src",soup,assets)  #.jpg
    findUrlsAssets("script","src",soup,assets)  #.js
    findUrlsAssets("link","href",soup,assets) #.css
    findUrlsAssets("video","src",soup,assets)    #.mp4 etc
    findUrlsAssets("audio","src",soup,assets)    #.mp3
    findUrlsAssets("embed","src",soup,assets)    #media
    findUrlsAssets("object","data",soup,assets)   #media
    findUrlsAssets("source","src",soup,assets)  #media
    # more such tags can be added

    for i in xrange(len(assets)):
        assets[i] = urlparse.urljoin(seed,assets[i])    # change relative url to absolute url
    pages.append(Page(seed,assets))

    if limit and d<=0:    #terminate search at cutoff depth
        return
    for link in urls:   # dfs
        link = urlparse.urljoin(seed,link)
        if link not in Crawled:
            startCrawling(link,d-1,limit)

def main():
    try:   
        depth = -1
        seed = raw_input("Enter seed url: ")

        url = urlparse.urlparse(seed)
        if not (seed.startswith("http://") or seed.startswith("https://")):     # if input url does not begin with http/https
            seed = "http://" + url[1] + url[2]

        infOrDepth = raw_input("Do you want to limit the search depth? [y/n]: ")
        if infOrDepth.startswith("y"):
            depth = int(raw_input("Enter depth: "))
            startCrawling(seed,depth,True)
        else:
            startCrawling(seed,depth,False)
    except (KeyboardInterrupt, SystemExit):
        pass

    jsonoutput = json.dumps([o.dump() for o in pages], default = set_default, indent = 2)
    f = open("output.txt","w")
    f.write(jsonoutput)
    f.close()

if __name__ == '__main__':
    main()