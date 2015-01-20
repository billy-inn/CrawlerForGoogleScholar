from scrapy.spider import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
from scrapy.http import Request
from crawler.ProxyPool import ProxyPool
from scrapy.http.cookies import CookieJar
import urllib, socket, time, random
import string

class Crwaler(Spider):
	name = "crawler"
	allowed_domains = ['scholar.google.com']
	#start_urls = ['http://scholar.google.com/citations?user=n1zDCkQAAAAJ']	

	def __init__(self):
		self.timepointer = int(time.clock())
		self.cnt = 0
		#self.limit = 100
		self.agents = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'
		#self.proxy = ''
		#self.proxy_usetime = 0
		#self.urlSet = set()
		#self.urlSet.add('n1zDCkQAAAAJ')
		#self.ReplaceProxy()
		f = open("author.txt").readlines()
		n = len(f)/3
		self.start_urls = []
		for i in range(2000,3000):
			ID = f[3*i+2].strip()
			url = 'http://scholar.google.com/citations?user=' + ID
			self.start_urls.append(url)

	def parse(self,response):
		cookieJar = response.meta.setdefault('cookie_jar',CookieJar())
		cookieJar.extract_cookies(response, response.request)
		header = response.headers

		sel = Selector(response)

		yield Request(response.url + '&cstart=0&pagesize=100', callback=self.CrawlData)

		#self.proxy_usetime += 1
		#if self.proxy_usetime > 3:
			#self.ReplaceProxy()

		#urlList = sel.xpath('//a[@class="gsc_rsb_aa"]/@href').extract()
		for url in []:#urlList:
			idx = url.find("user")
			_id = url[idx+5:idx+17]
			if _id in self.urlSet:
				continue
			else:
				self.urlSet.add(_id)
			self.cnt += 1
			if self.cnt <= self.limit: 
				#request = Request('http://scholar.google.com'+url, dont_filter=True, callback=self.parse,
				#				   meta={'User_agent':self.agents,
				#				   'proxy':self.proxy,
				#				   'cookie_jar':cookieJar})
				#cookieJar.add_cookie_header(request)
				#yield request
				yield Request('http://scholar.google.com'+url, callback=self.parse)

			#self.proxy_usetime += 1
			#if self.proxy_usetime > 3:
			#	self.ReplaceProxy()

	def CrawlData(self, response):
		if response.status == 200:
			sel = Selector(response)

			url = response.url
			idx = url.find("user")
			_id = url[idx+5:idx+17]

			item = CrawlerItem()
	
			item['_id'] = _id
			item['url'] = response.url
			item['name'] = sel.xpath('//div[@id="gsc_prf_in"]/text()').extract()[0]
			item['info'] = sel.xpath('//div[@class="gsc_prf_il"]/text()').extract()[0]
			tmp = sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract()
			item['pubs'] = []
			n = len(tmp)
			for i in range(1,n+1):
				pub = {}
				pub['title'] = \
					sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/a/text()' % i).extract()
				pub['author'] = \
					sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/div[1]/text()' % i).extract()
				pub['venue'] = \
					sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/div[2]/text()' % i).extract()
				pub['citation'] = \
					sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_c"]/a/text()' % i).extract()
				pub['year'] = \
					sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_y"]/span/text()' % i).extract()
				item['pubs'].append(pub)

			yield item
			
			if n == 100:
				offset = 0; d = 0
				idx = url.find('cstart=')
				idx += 7
				while url[idx].isdigit():
					offset = offset*10 + int(url[idx])
					idx += 1
					d += 1
				yield Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.CrawlData)
	
	def ReplaceProxy(self):
		print 'changing proxy'
		socket.setdefaulttimeout(3.0)
		test_url = 'http://scholar.google.com'
		while True:
			try:
				proxy = random.choice(ProxyPool)
				print proxy
			except:
				continue

			try:
				start = time.time()
				f = urllib.urlopen(test_url, proxies={'http':proxy})
				print f.read()
				f.close()
			except:
				continue
			else:
				end = time.time()
				dur = end - start
				print proxy, dur
				if dur <= 2:
					print 'proxy change to', proxy
					self.proxy = proxy
					self.proxy_usetime = 0
					break
				else:
					continue
	
