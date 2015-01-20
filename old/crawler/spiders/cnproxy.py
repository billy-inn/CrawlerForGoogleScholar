from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from crawler.items import ProxyItem

class Crawler(Spider):
	name = 'cnproxy'
	allowed_domains = ['www.cnproxy.com']
	start_urls = ['http://www.cnproxy.com/index.html']

	def parse(self,response):
		sel = Selector(response)

		otherpages = sel.xpath('//div[@id="plist"]/div[@class="intro"]/ul/li/a/@href').extract()

		for page in otherpages:
			yield Request('http://www.cnproxy.com/' + page,callback=self.crawl)
	
	def crawl(self,response):
		sel = Selector(response)

		ipList = sel.xpath('//table//tr/td[1][not(@width)]/text()').extract()
		portList = sel.xpath('//table//tr/td[1][not(@width)]/script/text()').extract()

		fw = open('cnproxy.txt','a')
		n = len(ipList)
		for i in range(n):
			proxy = ipList[i].strip() + ":"
			numcode = portList[i][19:-1]
			for j in range(0,len(numcode),2):
				proxy = proxy + self.char2num(numcode[j])
			fw.write('%s\n' % proxy)
		fw.close()

	def char2num(self,char):
		if char == "a": return "2"
		if char == "q": return "0"
		if char == "c": return "1"
		if char == "m": return "4"
		if char == "v": return "3"
		if char == "r": return "8"
		if char == "l": return "9"
		if char == "i": return "7"
		if char == "b": return "5"
		if char == "w": return "6"
		return "0"

