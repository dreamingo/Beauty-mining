# -- coding: utf-8 --

#Setting use in the global project
APP_KEY = "245283018"

APP_SECRET = "ef354980fddd9d6b78d9df1590ded3b4"

CALLBACK_URL = "https://api.weibo.com/oauth2/default.html"

ACCOUNT="404947851@qq.com"

PASSWORD="26651479"

BayesianSetting = {"comment_ps":0.6,
					"comment_ph":0.4,
					"name_ps":0.4,
					"name_ph":0.6,
					"description_ps":0.4,
					"description_ph":0.6,
					"comment_psmissword":0.9,
					"comment_phmissword":0.1,
					"name_psmissword":0.4,
					"name_phmissword":0.6,
					"description_psmissword":0.1,
					"description_phmissword":0.9,
					}
#Get the password from input stream
# print "weibo account:",ACCOUNT
# PASSWORD=getpass.getpass()

