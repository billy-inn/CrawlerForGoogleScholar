import urllib, time, socket
from ProxyPool import ProxyPool

#fr = open('proxyData/cnproxy.txt','r')
#proxyList = fr.readlines()
#fr.close()

socket.setdefaulttimeout(3.0)
test_url = 'http://scholar.google.com'

#fw = open('ProxyPool.txt','a')

for proxy in ProxyPool:
	proxy = 'http://' + proxy.strip()
	print proxy
	try:
		start = time.time()
		f = urllib.urlopen(test_url,proxies={'http':proxy})
		print f.read()
		f.close()
	except:
		continue
	else:
		end = time.time()
		dur = end - start
		print dur
		#if dur <= 10:
		#	fw.write('%s\n' % proxy)

fw.close()
