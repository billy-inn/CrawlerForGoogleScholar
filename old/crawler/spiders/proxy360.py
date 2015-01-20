from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from crawler.items import ProxyItem

class Crawler(Spider):
	name = 'proxy360'
	allowed_domains = ['www.proxy360.cn']
	start_urls = ['http://www.proxy360.cn']

	def parse(self,response):
		sel = Selector(response)

		otherpages = sel.xpath('//div[@class="region_item"]/a/@href').extract()

		for page in otherpages:
			yield Request(page,callback=self.crawl)
	
	def crawl(self,response):
		sel = Selector(response)

		ipList = sel.xpath('//div[@class="proxylistitem"]/div/span[1]/text()').extract()
		portList = sel.xpath('//div[@class="proxylistitem"]/div/span[2]/text()').extract()

		fw = open('proxy360.txt','a')
		n = len(ipList)
		for i in range(n):
			proxy = ipList[i].strip() + ":" + portList[i].strip()
			fw.write('%s\n' % proxy)
		fw.close()

