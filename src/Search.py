#-- coding=utf-8 --
import json
import urllib
import re 
import urllib2
import cookielib
import cPickle
import re import cPickle
import configure
import math
import random
import os
from bayesFilter import bayesFilter as bayesFilter
from searchNode import searchNode as searchNode


'''有序插入'''
def insertOrderly(searchList, node):
	position = len(searchList);
	for i in xrange(0, len(searchList)):
		if searchList[i].getValue() < node.getValue():
			position = i
			break
	searchList.insert(position, node)

'''返回是否应该搜索这个节点'''
def searchOrNot(item, idList, namefilter, descriptionFilter, invalidName, invalidDescription, validName, validDescription):

	# 不是女的禁止搜索
	if item["gender"] != "f":
		return False

	if item["id"] in idList:
		return False

	# 已经加V的禁止搜索（防止各种官方微薄或名人等）
	if item["verified"] == True:
		return False
	# 粉丝数目大于20000禁止搜索
	if item["followers_count"] > 20000:
		return False
	#关注小于250的禁止搜索（一个正常的微博控怎么可能关注这么少人呢）
	if item["friends_count"] < 250:
		return False

	if namefilter.myFilter(item["name"].encode("utf-8")):
		invalidName.write(item["name"].encode("utf-8") + "\n")
		# print item["name"] + " is invalid!!!!"
		return False
	else:
		validName.write(item["name"].encode("utf-8") + "\n")


	if len(item["description"]) !=0 and descriptionFilter.myFilter(item["description"].encode("utf-8")):
		invalidDescription.write(item["description"].encode("utf-8")+ "\n")
		# print item["description"] + " is invalid!!!!"
		return False
	else:
		validDescription.write(item["description"].encode("utf-8")+ "\n")
	return True

'''用于输出调试信息'''
def print_searchList(searchList, filename):
	fileptr = file(filename,"w+a")

	print "++++++++++++++++++++++++++++++++++++++++++++++++++++="
	fileptr.write("++++++++++++++++++++++++++++++++++++++++++++\n")

	for i in searchList:
		s = json.dumps(i.getParentList(), encoding="UTF-8", ensure_ascii=False)
		fileptr.write(i.getName() + " " + str(i.getValue()) + " " + i.getGradeInfo() + "       " + s.encode("utf-8") + "\n") 
		print i.getName(), i.getValue()

	print "++++++++++++++++++++++++++++++++++++++++++++++++++++="
	fileptr.write("++++++++++++++++++++++++++++++++++++++++++++\n")
	print len(searchList)
	fileptr.write(str(len(searchList)))

'''一号调度系统，使用类似pagerank 算法中，处理spider trap的思想
每走一步，有w的概率选择头元素， 有1-w的概率， 直接跳往第一层开荒。
'''
def schedule1(searchList):
	k = random.randint(1,10)
	if k <=1:
		for i in range(1,4):
			for j in xrange(0,len(searchList)):
				if len(searchList[j].getParentList()) == i:
					print "Jump to ", searchList[j].getName()
					return j
	else:
		return 0



'''2号调度系统，维护一张最近使用的父节点列表，
#如果有使用，则增加次数，次数达到某一个值将会被锁上，并且惩罚一段时间后才被解封
#如果没有被使用，则aging。
'''
def isOK(parentList, name, recentlyUsedList):
	OK = True
	# if the directson never exisit, then add it
	if len(parentList) == 0:
		return True

	if len(parentList) == 1:
		recentlyUsedList[name] = 0
		tmpkey = name
	
	else:
		tmpkey = parentList[1]
		if recentlyUsedList[tmpkey] < 0:
			print tmpkey + "is lock!!!!!!!!!!!!!!!!!!!!!!!!!!!"
			return False

		# if the use frequency  greater than 5, lock it
		elif recentlyUsedList[tmpkey] > 7:
			# lock it, and every time add it until it up to -1, then set it to 3
			recentlyUsedList[tmpkey] = -5
			return False
		else:
			recentlyUsedList[tmpkey] += 3

	# Aging
	for i in recentlyUsedList:
		if recentlyUsedList[i] == -1:
			print i + "is unlock~~~~~~~~"
			recentlyUsedList[i] = 3

		elif recentlyUsedList[i] >= 0 and i != tmpkey: 
			recentlyUsedList[i] -=1
			if recentlyUsedList[i] < 0:
				recentlyUsedList[i] = 0

		elif recentlyUsedList[i] < -1:
			recentlyUsedList[i] +=1

	print  "========================="
	for i in recentlyUsedList:
		print i, recentlyUsedList[i]
	print  "========================="
	return OK

def schedule2(searchList, recentlyUsedList):
	for i in xrange(0,len(searchList)):
		parentList = searchList[i].getParentList()
		name = searchList[i].getName()
		if isOK(parentList, name, recentlyUsedList):
			return i
# ====================================================

'''Seach Model'''
def search(client):

	nameFilter = bayesFilter("name")
	descriptionFilter = bayesFilter("description")
	recentlyUsedList =  {}

	APIUseCount = 0
	searchList = []
	#加入根节点 准备搜索
	root_uid = client.get.account__get_uid()
	root_info = client.get.users__show(uid=root_uid["uid"])
	searchList.append(searchNode(root_info, ()))

	fileptr = file("../debugInfo/consoleInfo.dat", "w")

	invalidName = file("../debugInfo/invalidName.dat", "w")
	validName = file("../debugInfo/validName.dat", "w")
	invalidDescription= file("../debugInfo/invalidDescription.dat", "w")
	validDescription= file("../debugInfo/validDescription.dat", "w")
	count = 0;
	userList = []
	idList = set()

	successFlag = True
	# 用来记录最近搜索的节点, 如果长期7一个森林里面游荡,强行请出..
	recent_search = []

	try:
		while(len(userList) < 5000 and len(searchList)):

			#Schedule function1
			# topNodenum = schedule2(searchList, recentlyUsedList)
			topNodenum = schedule1(searchList)
			topNode = searchList[topNodenum]
			del searchList[topNodenum]
			recent_search.append(topNode)

			# debug 信息 
			count +=1
			print "len(searchList): ", len(searchList)
			s = json.dumps(topNode.getParentList(), encoding="UTF-8", ensure_ascii=False)
			fileptr.write(str(count) + " "+ topNode.getName() + " " + str(topNode.getValue())+" "+str(topNode.getGradeInfo()) + " " + s.encode("utf-8") + "\n")
			print str(count) + " "+ topNode.getName() + " " + str(topNode.getValue()) + "     " + s.encode("utf-8")
			# =============================================================================

			parentList = topNode.getParentList()
			#保证只搜索4层之内的东西

			if len(parentList) <=3:
				friends = client.get.friendships__friends(count=200, uid=topNode.getUid())
				APIUseCount +=1
				print "APIUseCount", APIUseCount
				topNode.setFriendsList(friends["users"])
				for eachitem in friends["users"]:
					# 满足搜索条件
					if searchOrNot(eachitem, idList, nameFilter, descriptionFilter, invalidName, invalidDescription, validName, validDescription):
						tempList = list(parentList)
						tempList.append(topNode.getName())
						tempNode = searchNode(eachitem, tempList)
						#evaluate the tempnode value, the bigger, the better
						tempNode.evaluate()
						#Insert the node into the search list according to the evaluated value;
						insertOrderly(searchList,tempNode)
						insertOrderly(userList,tempNode)
						idList.add(eachitem["id"])

	except Exception as ex:
		successFlag = False
		userListptr = file("../debugInfo/UserlistPickle", "w")
		searchListptr = file("../debugInfo/searchlistPickle", "w")

		cPickle.dump(userList, userListptr)
		cPickle.dump(searchList, userListptr)

		print_searchList(userList, "../debugInfo/userList")
		print "Error!!!"
		print "APIUseCount", APIUseCount
		print "======================================"
		print ex

	if successFlag:
		userListptr = file("../debugInfo/UserlistPickle", "w")
		cPickle.dump(userList, userListptr)
		print_searchList(userList, "../debugInfo/userList")
		print "APIUseCount", APIUseCount
