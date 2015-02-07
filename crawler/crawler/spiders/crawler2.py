from scrapy.spider import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
from scrapy.http import Request
from datetime import datetime, timedelta
import string, random
import pymongo
from bson import ObjectId
import urllib, socket
import time

class Crawler(Spider):
	name = "2"
	allowed_domains = ['scholar.google.com']

	def __init__(self):
		self.db = pymongo.Connection('ip',123)['name']
		self.db.authenticate('username',"password")
		conf = open("conf").readlines()
		profile_db = conf[1].strip()
		self.profile = self.db[profile_db]
		self.start_urls = []
		self._id = {}
		#self.idList = []
		self.ptr = int(conf[0].strip())
		t = datetime.now()
		tmp = {'year':t.year, 'month':t.month, 'day':t.day, 'hour':t.hour, 
			   'minute':t.minute, 'second':t.second, 'microsecond':t.microsecond}
		fr = open("id.txt").readlines()
		for i in range(self.ptr, len(fr)):
			_id = ObjectId(fr[i].strip())
			self.entry = self.profile.find_one({"_id":_id})
			if not self.isVaild(tmp):
				self._id[self.entry["ID"]] = self.entry["_id"]
				self.start_urls.append(self.entry['url'] + '&cstart=0&pagesize=100')
		self.proxies = []
		self.request100proxy = 'http://erwx.daili666.com/ip/?tid=559592762367605&num=100&filter=on&foreign=only'
		self.request1proxy = 'http://erwx.daili666.com/ip/?tid=559592762367605&num=1&filter=on&foreign=only'
		proxy = urllib.urlopen(self.request100proxy)
		for line in proxy.readlines():
			self.proxies.append('http://' + line.strip())
		#self.limit = len(self.idList)
		#self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
		#while self.isVaild(tmp):
		#	print "Skip %s" % str(self.entry["_id"])
		#	self.ptr += 1
		#	if self.ptr >= self.limit:
		#		self.entry = None
		#		break
		#	self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
		#if self.entry is not None:
		#	self.entry['token'] = tmp
		#	self.entry['pubs'] = []
		#	self.start_urls = [self.entry['url'] + '&cstart=0&pagesize=100',]
		#	print "Start Processing %s" % str(self.entry["_id"])
	
	def choose_proxy(self):
		idx = random.randint(0, 99)
		if not self.test_proxy(self.proxies[idx]):
			proxy = urllib.urlopen(self.request1proxy)
			self.proxies[idx] = 'http://' + proxy.readlines()[0].strip()
		return self.proxies[idx]
	
	def test_proxy(self, proxy):
		socket.setdefaulttimeout(3.0)
		test_url = 'http://scholar.google.com'
		try:
			f = urllib.urlopen(test_url, proxies={'http':proxy})
		except:
			return False
		else:
			if f.getcode() != '200':
				return False
			else:
				return True
	
	def make_requests_from_url(self,url):
		return Request(url, callback=self.parse, meta={'proxy'=self.choose_proxy()})

	def parse(self,response):
		sel = Selector(response)

		url = response.url
		idx = url.find("user")
		_id = url[idx+5:idx+17]

		item = CrawlerItem()
	
		item['_id'] = self._id[_id]
		#item['ID'] = _id
		#item['url'] = response.url
		#item['name'] = sel.xpath('//div[@id="gsc_prf_in"]/text()').extract()[0]
		#item['info'] = sel.xpath('//div[@class="gsc_prf_il"]/text()').extract()[0]
		t = datetime.now()
		item['token'] = {'year':t.year, 'month':t.month, 'day':t.day, 'hour':t.hour, 
						 'minute':t.minute, 'second':t.second, 'microsecond':t.microsecond}
		tmp = sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract()
		item['pubs'] = []
		n = len(tmp)
		for i in range(1,n+1):
			pub = {}
			pub['title'] = \
				sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/a/text()' % i).extract()
			pub['url'] = \
				sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/a/@href' % i).extract()
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
			yield Request(url[:idx-d] + str(offset+100) + '&pagesize=100', callback = self.parse, meta={'proxy'=self.choose_proxy()})
		#else:
		#	item["entry"] = self.entry
		#	yield item
		#	self.ptr += 1
		#	if self.ptr >= self.limit:
		#		self.entry = None
		#	else:
		#		self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
		#	while self.isVaild(item['token']):
		#		print "Skip %s" % str(self.entry["_id"])
		#		self.ptr += 1
		#		if self.ptr >= self.limit:
		#			self.entry = None
		#			break
		#		self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
		#	if self.entry is not None:
		#		self.entry['token'] = item['token']
		#		self.entry['pubs'] = []
		#		yield Request(self.entry['url'] + '&cstart=0&pagesize=100', callback = self.parse, meta={'proxy'='http://localhost:3128'})
		#		print "Start Processing %s" % str(self.entry["_id"])
	
	def isVaild(self, new):
		if self.entry is None:
			print "Invaild item"
			return False
		if not self.entry.has_key("token"):
			print "No token"
			return False
		t = self.entry["token"]
		old = datetime(t['year'], t['month'], t['day'], t['hour'],
					   t['minute'], t['second'], t['microsecond'])
		t = new
		new = datetime(t['year'], t['month'], t['day'], t['hour'],
					   t['minute'], t['second'], t['microsecond'])
		d = new - old
		print "Have passed %d days after last update" % d.days
		return d.days <= 30
