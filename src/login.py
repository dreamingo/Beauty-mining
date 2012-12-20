#coding=utf8
from weibo import APIClient
import httplib
import urllib
import configure
import getpass
import urllib2
import cookielib
import base64
import re
import json
import hashlib


#使用微薄API，用浏览器模拟授权过程
# ============================================================================
client  = APIClient(app_key=configure.APP_KEY, app_secret = configure.APP_SECRET, redirect_uri=configure.CALLBACK_URL)
url = client.get_authorize_url()


def get_code():
	conn = httplib.HTTPSConnection('api.weibo.com')
	postdata = urllib.urlencode ({'client_id':configure.APP_KEY,'response_type':'code','redirect_uri':configure.CALLBACK_URL,'action':'submit','userId':configure.ACCOUNT,'passwd':configure.PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
	conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
	res = conn.getresponse()
	# print 'msg===========',res.msg
	# print 'status===========',res.status
	# print 'reason===========',res.reason
	# print 'version===========',res.version
	headers = res.getheaders()
	location = res.getheader('location')
	code = location.split('=')[1]
	conn.close()
	return code

def APILogin():
	r = client.request_access_token(get_code())
	client.set_access_token(r.access_token, r.expires_in)
	return  client


# 直接用浏览器模拟整个登录过程
# =============================================================
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
postdata = {
		'entry': 'weibo',
		'gateway': '1',
		'from': '',
		'savestate': '7',
		'userticket': '1',
		'ssosimplelogin': '1',
		'vsnf': '1',
		'vsnval': '',
		'su': '',
		'service': 'miniblog',
		'servertime': '',
		'nonce': '',
		'pwencode': 'wsse',
		'sp': '',
		'encoding': 'UTF-8',
		'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
		'returntype': 'META'
		}

def get_servertime():
	url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
	data = urllib2.urlopen(url).read()
	p = re.compile('\((.*)\)')
	try:
		json_data = p.search(data).group(1)
		data = json.loads(json_data)
		servertime = str(data['servertime'])
		nonce = data['nonce']
		return servertime, nonce
	except:
		print 'Get severtime error!'
		return None

def get_pwd(pwd, servertime, nonce):
	pwd1 = hashlib.sha1(pwd).hexdigest()
	pwd2 = hashlib.sha1(pwd1).hexdigest()
	pwd3_ = pwd2 + servertime + nonce
	pwd3 = hashlib.sha1(pwd3_).hexdigest()
	return pwd3

def get_user(username):
	username_ = urllib.quote(username)
	username = base64.encodestring(username_)[:-1]
	return username


def browserLogin():
	username = configure.ACCOUNT
	pwd = configure.PASSWORD
	url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
	try:
		servertime, nonce = get_servertime()
	except:
		return
	global postdata
	postdata['servertime'] = servertime
	postdata['nonce'] = nonce
	postdata['su'] = get_user(username)
	postdata['sp'] = get_pwd(pwd, servertime, nonce)
	postdata = urllib.urlencode(postdata)
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

	req  = urllib2.Request(
			url = url,
			data = postdata,
			headers = headers
			)
	result = urllib2.urlopen(req)
	text = result.read()

	p = re.compile('location\.replace\(\'(.*?)\'\)')
	try:
		login_url = p.search(text).group(1)
		print login_url
		urllib2.urlopen(login_url)
		# print "login success!"
	except:
		print 'Login error!'
