import urllib, time, socket

fr = open('proxyData/cnproxy.txt','r')
proxyList = fr.readlines()
fr.close()

socket.setdefaulttimeout(3.0)
test_url = 'http://scholar.google.com'

fw = open('ProxyPool.txt','a')

for proxy in proxyList:
	proxy = 'http://' + proxy.strip()
	print proxy
	try:
		start = time.time()
		f = urllib.urlopen(test_url,proxies={'http':proxy})
		f.close()
	except:
		continue
	else:
		end = time.time()
		dur = end - start
		print dur
		if dur <= 10:
			fw.write('%s\n' % proxy)

fw.close()
