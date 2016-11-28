**** REQUIREMENTS ****
1. BeautifulSoup installation
	---- *NIX
	$ apt-get install python-bs4
	$ easy_install beautifulsoup4
	$ pip install beautifulsoup4	(unix)
	$ python setup.py install

	---- Windows
	Download from here - https://www.crummy.com/software/BeautifulSoup/bs4/download/
	Run - python setup.py install - in the directory where you have unzipped the folder

**** RUNNING THE SCRIPT ****
1. python crawler.py
	---- You can:
	a. Search up to a fixed depth rather than waiting for (almost) an infinite time!
	b. Ctrl-C to anytime exit the script and the crawled webpages will not be lost!
	c. Check output.txt to see what pages you've crawled to!
	d. Set the proxy settings (if required) at line #11. Explained with example.