from scrapy.spider import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
from scrapy.http import Request
from datetime import datetime, timedelta
import string
import pymongo
from bson import ObjectId

class Crawler(Spider):
	name = "2"
	allowed_domains = ['scholar.google.com']

	def __init__(self):
		self.db = pymongo.Connection('ip',123)['name']
		self.db.authenticate('username',"password")
		conf = open("conf").readlines()
		profile_db = conf[1].strip()
		self.profile = self.db[profile_db]
		self.idList = []
		self.ptr = int(conf[0].strip())
		fr = open("id.txt")
		for item in fr.readlines():
			self.idList.append(ObjectId(item.strip()))
		self.limit = len(self.idList)
		self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
		t = datetime.now()
		tmp = {'year':t.year, 'month':t.month, 'day':t.day, 'hour':t.hour, 
			   'minute':t.minute, 'second':t.second, 'microsecond':t.microsecond}
		while self.isVaild(tmp):
			print "Skip %s" % str(self.entry["_id"])
			self.ptr += 1
			if self.ptr >= self.limit:
				self.entry = None
				break
			self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
		if self.entry is not None:
			self.entry['token'] = tmp
			self.entry['pubs'] = []
			self.profile.save(self.entry)
			self.start_urls = [self.entry['url'] + '&cstart=0&pagesize=100',]
			print "Start Processing %s" % str(self.entry["_id"])

	def parse(self,response):
		sel = Selector(response)

		url = response.url
		idx = url.find("user")
		_id = url[idx+5:idx+17]

		item = CrawlerItem()
	
		item['_id'] = self.entry['_id']
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

		self.entry['pubs'].extend(item['pubs'])
		self.profile.save(self.entry)
			
		if n == 100:
			offset = 0; d = 0
			idx = url.find('cstart=')
			idx += 7
			while url[idx].isdigit():
				offset = offset*10 + int(url[idx])
				idx += 1
				d += 1
			yield Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.parse)
		else:
			self.ptr += 1
			if self.ptr >= self.limit:
				self.entry = None
			else:
				self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
			while self.isVaild(item['token']):
				print "Skip %s" % str(self.entry["_id"])
				self.ptr += 1
				if self.ptr >= self.limit:
					self.entry = None
					break
				self.entry = self.profile.find_one({"_id":self.idList[self.ptr]})
			if self.entry is not None:
				self.entry['token'] = item['token']
				self.entry['pubs'] = []
				self.profile.save(self.entry)
				yield Request(self.entry['url'] + '&cstart=0&pagesize=100', callback = self.parse)
				print "Start Processing %s" % str(self.entry["_id"])
	
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
