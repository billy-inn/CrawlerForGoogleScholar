# Crawler for Google Scholar

### Prerequsites

- Scrapy

### Crawl the author network

Enter following code in command line:

    scrapy crawl crawler -o name.json -t json

Then you will get the result in the format of json in *name.json*.

### Crawl the proxies

Crawl from www.proxy360.cn:

    scrapy crawl proxy360

Then the proxy list can be found in *proxy360.txt*.

Crawl from www.cnproxy.com:

    scrapy crawl cnproxy

Then the proxy list can be found in *cnproxy.txt*.

### Get the effective proxies list

    python test.py
	python generate.py

### Setting

You can change the **limit** in *Crawler.py* to set the maximal amount of authors crawled.

You can change the **DOWNLOAD_DELAY** in *settings.py* to set the delay time between the crawling of pages.
