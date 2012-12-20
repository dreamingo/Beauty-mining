#coding=utf-8

import urllib
import re
import bs4
import HTMLParser
import html5lib
import datetime
import login
import urllib2
import chardet
import base62

def extractRawData(text):
	re_h=re.compile('</?\w+[^>]*>')

	'''从script中提取内容'''
	soup = bs4.BeautifulSoup(text)
	t = soup.select("script")
	s = ""
	for text in t:
		if str(text).find('"pid":"pl_content_weiboDetail"') >0:
			s = str(text)
			break
	if s == "":
		print "extract error!"
		return []
	start = s.find("html")
	start+=7
	end = s.find('"})</script')
	s = s[start:end]
	s = re.sub(r"\\\/","/", s)
	s = re.sub(r"\\t", "	",s)
	s = re.sub(r"\\n", "\n",s)
	s = re.sub(r"&lt;", "<",s)
	s = re.sub(r"&gt;", ">",s)
	s = re.sub(r'\\"', '"',s)
	s = re.sub(r'&amp;', '&',s)

	'''页面解析'''
	'''Get the tweetContent'''
	soup1=bs4.BeautifulSoup(s,"html5lib")
	contents=soup1.find_all("div", {"class":"WB_text"})

	for i in contents:
		soup2=bs4.BeautifulSoup(str(i),from_encoding="utf-8")
		# soup2=bs4.BeautifulSoup(str(i))
		tweet=soup2.findAll('em')
		tweetContent=re_h.sub('',str(tweet[0]))
		print 'tweetContent:%s' % tweetContent

		author = re.findall('nick-name="(.*)"', str(tweet[0]))
		# print 'author:%s' % author[0]  #weibo作者
	
	comment_lists = soup1.find_all("dl",{"class":"comment_list S_line1"})

	result_lists = []
	for i in comment_lists:
		comment = ""
		soup2=bs4.BeautifulSoup(str(i),from_encoding="utf-8")
		dd = soup2.find("dd")
		soup3=bs4.BeautifulSoup(str(dd),from_encoding="utf-8")
		date = soup3.find("span", {"class":"S_txt2"})
		img = soup3.find_all("img")

		comment += dd.contents[1].text.encode("utf-8")

		for i in xrange(2, len(dd.contents)):
			if dd.contents[i] != date:
				if dd.contents[i] in img:
					pic = re.findall('alt="\[(.*)\]" src', str(dd.contents[i]))
					if len(pic) > 0:
						comment += str(pic[0])
				else:
					try:
						comment += dd.contents[i].text.encode("utf-8")
					except Exception as ex:
						comment += dd.contents[i].encode("utf-8")
			else:
				break
		if comment.find("：") != -1:
			comment = comment.split("：")[1]
		if comment.find(":") != -1:
			comment = comment.split(":")[1]
		result_lists.append(comment)
	return result_lists




def getComment(mid, uid):
	wid = base62.mid2str(mid)
	url1 = "http://weibo.com/"+str(uid)+"/"+wid
	print url1
	req = urllib2.Request(url=url1,)
	result = urllib2.urlopen(req)
	text = result.read()
	return extractRawData(text)

if __name__ == "__main__":
	login.browserLogin()
	url1 = "http://weibo.com/1893496911/z7qzHsUQX"
	req = urllib2.Request(url=url1,)
	result = urllib2.urlopen(req)
	encoding = result.headers.getparam('charset')
	text = result.read()
	extractRawData(text)
