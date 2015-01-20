fr = open('ProxyPool.txt')
fw = open('ProxyPool.py','w')
fw.write('ProxyPool = [')

for line in fr.readlines():
	fw.write("\'%s\',\n" % line.strip())

fw.write(']\n')
fw.close()
fr.close()
