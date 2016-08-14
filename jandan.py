import urllib.request
import os
import io
import sys
import random
import time
from bs4 import BeautifulSoup
from threading import Thread
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #控制台中文乱码解决方案

def responsehtml(url):
	n1=str(random.randint(1, 254))+"."
	n2=str(random.randint(1, 254))+"."
	n3=str(random.randint(1, 254))+"."
	n4=str(random.randint(1, 254))
	print (n1+n2+n3+n4)
	headers = {
	'Upgrade-Insecure-Requests' : '1',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2725.0 Safari/537.36',
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	#'Accept-Encoding' : 'gzip, deflate',
	'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
	'Connection' : 'keep-alive',
	'Content-Length' : '0',
	'X-Forwarded-For': n1+n2+n3+n4,
	'Client-Ip':n1+n2+n3+n4,
	'Cache-Control':'max-age=0',
	'DNT':'1',
	'Host':'jandan.net',
	'Upgrade-Insecure-Requests':'1'
	}
	req = urllib.request.Request(url=url, headers=headers)
	try:
		return urllib.request.urlopen(req).read()#return Bytes
	except urllib.request.HTTPError as e:
		print (e.code)

def bs(html):
	soup = BeautifulSoup(html, 'lxml')
	imglist = soup.find_all("a", class_="view_img_link")
	nextlist = soup.find_all("a", class_="previous-comment-page")
	for i in imglist:
		#print (i['href'])
		try:
			t = Thread(target=downloadthread, args=(i['href'],))
			t.start()
		except:
			print ("THread start fail")
	if nextlist:
		return nextlist[0]['href']

def downloadthread(i):
	global j
	j = j+1
	jpgpathname = 'D:\\jandan\\'+ str(j) +"---"+ os.path.basename(i)
	try:
		urllib.request.urlretrieve(i, jpgpathname)
		#print ("Download OK!!!")
	except:
		print ("Download fail!!!")

#main-----------------------------
j = 0
url = 'http://jandan.net/ooxx'
html = responsehtml(url)

while 1:
	nexturl = bs(html)
	html = responsehtml(nexturl)
	print(nexturl)
	if not nexturl:
		break

print ("main thread exit!")


'''
print (type(html))
#html = html.read()
print (type(html))

html = str(html)
print (type(html))


#print (html)
#jpgpathname = 'D:\\jandan\\'+time.strftime("%Y-%m-%d", time.localtime())+".jpg"
#urllib.request.urlretrieve(jpgurl, jpgpathname)
'''
