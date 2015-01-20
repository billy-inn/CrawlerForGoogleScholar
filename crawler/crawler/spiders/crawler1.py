from scrapy.spider import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
from scrapy.http import Request
import string

class Crawler(Spider):
	name = "1"
	allowed_domains = ['scholar.google.com']

	def __init__(self):
		start_url = open("conf").readlines()[0].strip()
		self.start_urls = [start_url,]
		self.urlSet = set()

	def parse(self,response):
		sel = Selector(response)

		url = response.url
		idx = url.find("user")
		_id = url[idx+5:idx+17]

		item = CrawlerItem()

		item['_id'] = _id
		item['url'] = url
		item['name'] = sel.xpath('//div[@id="gsc_prf_in"]/text()').extract()[0]
		item['info'] = sel.xpath('//div[@class="gsc_prf_il"]/text()').extract()[0]
		item['pubs'] = []

		yield item
		
		urlList = sel.xpath('//a[@class="gsc_rsb_aa"]/@href').extract()
		for url in urlList:
			idx = url.find("user")
			_id = url[idx+5:idx+17]
			if _id in self.urlSet:
				continue
			else:
				self.urlSet.add(_id)
			yield Request('http://scholar.google.com'+url, callback=self.parse)
