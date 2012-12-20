#coding=utf-8
import math
import isbeauty
import urllib
import urllib2
import cookielib
import re
import os
import json


# 搜索节点的模板定义
# ==================================
# Return the picnum of ones album
def getPicnum(uid):
	url1 = "http://photo.weibo.com/"
	url1 += str(uid)
	url1 += "/profile/photo#http%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Ftrans.html%3F_wv%3D5%23STK_photoHeight!"

	req = urllib2.Request(url=url1,)
	result = urllib2.urlopen(req)
	text = result.read()
	count = re.findall('<span class="count">共(\d*)张</span>', text)
	return count


class searchNode:
	# 构造函数
	# =================
	def __init__(self, info, parent_list):
		self.info = info 
		self.parent_list = parent_list 
		self.value = 0;
		self.friends_followers = 0
		self.picnum = 0
		self.avatar = 0

	# 评估函数
	# =================
	def evaluate(self):
		statuses_count = self.info["statuses_count"]
		followers_count = self.info["followers_count"]
		friends_count = self.info["friends_count"]

		#粉丝与好友比例
		if friends_count ==0 :
			self.friends_followers = 0
		else:
			self.friends_followers = float(followers_count)/friends_count
			if self.friends_followers > 20:
				self.friends_followers = 15
			self.friends_followers *=8

		# 评估一个人所发微薄中，带有原创性图片的比例
		count = getPicnum(self.info["id"])

		if statuses_count != 0:
			if len(count) != 0:
				self.picnum = float(count[len(count)-1])/statuses_count
			else:
				self.picnum = 0
			if self.picnum > 0.5:
				if statuses_count < 200:
					self.picnum = 0.3 - float(200-statuses_count)/2000
			self.picnum *=200

		# 头像相册的大小
		if len(count) != 0:
			self.avatar = float(count[0])*5
			if self.avatar > 100:
				self.avatar = 100
		else:
			self.avatar = 5
		self.value = self.avatar + self.friends_followers + self.picnum + (4 - len(self.parent_list))*20

	# 获取微博
	# ====================================
	def getStatuses(self, client, num, errorInfoRecord):
		try:
			s = json.dumps(self.getParentList(), encoding="UTF-8", ensure_ascii=False)
			information = self.getName() + " " + str(self.getValue()) + " " + self.getGradeInfo() + "       " + s.encode("utf-8") + "\n" 
			count = 1
			dirpath = "../img/" + str(num) + self.getName()
			fileptrname = dirpath + "/info.dat"

			if not os.path.exists(dirpath):
				os.mkdir(dirpath)

			fileptr = file(fileptrname, "w")
			fileptr.write(information)

			isBeauty = isbeauty.isbeauty()
			self.statuses = []
			print self.info["statuses_count"]
			for i in range(0, int(math.ceil(float(self.info["statuses_count"])/100))):
				user_timeline = client.get.statuses__user_timeline(uid=self.getUid(), count=100,feature=1, page=i+1);
				for eachTimeline in user_timeline["statuses"]:
					if eachTimeline.has_key("original_pic"):
						print "Judgeing " + self.getName() + " " + str(count) + "weibo"
						# 用isBeauty判断器来判断是否是美女zipaizhao
						if isBeauty.judge(eachTimeline, client):
							# imgurl = eachTimeline["thumbnail_pic"]
							imgurl = eachTimeline["original_pic"]
							if imgurl.find("gif") == -1:
								type_name = ".jpg"
							else:
								type_name = ".gif"
							filename = dirpath + "/" + str(count) + type_name 
							urllib.urlretrieve(imgurl, filename)
							print filename + " download OK!"
							count +=1
		except Exception as ex:
			print ex
			errorInfoRecord.write(str(num) + "\n")

	# 各种get的小函数
	# ===============================
	def setFriendsList(self, friendlist):
		self.friendlist = friendlist

	def getBi_rate(self):
		return float(self.info["bi_followers_count"])/self.info["friends_count"]

	def getInfo(self):
		return self.info
	def getGradeInfo(self):
		temp = "ff: " + str(self.friends_followers) + "   picnum: " + str(self.picnum) + "  avatar:" + str(self.avatar)
		return temp

	def getValue(self):
		return self.value
	def getUid(self):
		return self.info["id"]
	def getParentList(self):
		temp_parent_list = list(self.parent_list);
		return temp_parent_list
	def getName(self):
		return self.info["name"].encode("utf-8")

# ==========================================================


