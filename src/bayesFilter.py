#coding=utf-8
import cPickle
import configure
import jieba
import math

class bayesFilter:

	def __init__(self, bayesType):
		self.bayesType = bayesType
		stopwordsFile = file("../data/stopword.txt", "r")
		line = stopwordsFile.readline()
		self.stopwordList = line.split("/")

		#从文件中load出词语概率表
		probabilityTableName = "../data/" + bayesType + "WordProbabilityTable.dat"
		try:
			fileProbabilityTable = file(probabilityTableName, "r")
		except Exception as ex:
			print "Load wordProbabilityTable Fail!"
			return 
		self.wordProbabilityTable = cPickle.load(fileProbabilityTable)
		#从配置文件中导入特定类型bayes Filter的ps/ph 配置
		self.ps = configure.BayesianSetting[bayesType + "_ps"]
		self.ph = configure.BayesianSetting[bayesType + "_ph"]
		self.psMissWord = configure.BayesianSetting[bayesType + "_psmissword"]
		self.phMissWord = configure.BayesianSetting[bayesType + "_phmissword"]
	
	'''对输入字符串进行归类'''
	def myFilter(self, string):
		tags = list(jieba.cut(string, cut_all=0))
		word_probability = {}
		pSpam = math.log(self.ps)
		pHealth = math.log(self.ph)
		word_valid = False
		#If the string all composited of all stopwords then it's invalid

		for word in tags:
			if word.encode("utf-8") not in self.stopwordList:
				word_valid = True
				if word in self.wordProbabilityTable:
					tmps = self.wordProbabilityTable[word]
					tmph = 1 - tmps
				else:
					tmps = self.psMissWord
					tmph = self.phMissWord

				if not word_probability.has_key(word):#重复的单词只算一次
					word_probability[word] = str(tmps) + "  " + str(tmph)
					# pSpam = tmps * pSpam
					# pHealth = tmph * pHealth 
					#用log相加减少误差
					pSpam += math.log(tmps)
					pHealth += math.log(tmph)

		#如果一句话中,全部都是stopwords,如果是名字,则认为是ok, 如果是评论则直接认为是spam
		if not word_valid:
			if self.bayesType == "comment":
				return True 
			else:
				return False
		if pSpam > pHealth:
			return True
		else:
			# statitics[string] = math.fabs(pSpam - pHealth)/(pSpam + pHealth)*100
			return False


if __name__=="__main__":
	commentFilter = bayesFilter("comment")
	# fileptr = file("info3/invalidComment.bat", "r")
	fileptr = file("../debugInfo/invalidComment", "r")
	validfileptr = file("../debugInfo/validComment", "r")
	# file11 = file("../debugInfo/tmprecord", "w")
	invalidLines = fileptr.readlines()
	validLines = validfileptr.readlines()
	invalidLines = [line.rstrip() for line in invalidLines]
	validLines = [line.rstrip() for line in validLines]
	# invalidchange = file("info3/invalidName.dat", "w")

	counter = 0
	print "Total invalidLine: ", len(invalidLines)
	# for line in validLines:
	# 	if commentFilter.myFilter(line):
	# 		counter+=1
			# print line
			# file11.write(line + "\n")
			# invalidchange.write(line+"\n")

	print "error detect: ",21015


