#coding=utf-8
import math
import cPickle
import jieba
import configure

# 用于校准没有出现过的词语
laplaceValue = 0.01

'''给定训练词库 valid*.txt 和 invalid*.txt
   利用jieba分词系统进行分词.对每个词语, 计算出
	   p(s|w) = p(w|s)*p(s)/(p(w|s)*p(s) + p(w|h)*p(h))
			其中, s代表 spam, h代表 health, w代表word词语
			p(s|w) 文章出现已知的词语w, 被判定为spam的概率
			p(w|s) 表示word在spam中出现的概率
			p(w|h) 表示word在health出现的概率
			p(s) 表示现实中, 一个文档是spam的概率.
			p(h) 表示现实中, 一个文档是health的概率.

   得到一张对应的wordProbabilityTable的哈希表
   dump到文件中, 以供后续使用.
'''
class bayesTrain:

	def __init__(self, validTrainData, invalidTrainData, bayesType):

		stopwordsFile = file("../data/stopword.txt", "r")
		line = stopwordsFile.readline()
		self.stopwordList = line.split("/")

		self.validTrainData = validTrainData
		self.invalidTrainData = invalidTrainData

		# 获取每份训练数据的词频表以及词数
		self.invalidWordsTotal, self.invalidWordsCountTable = self.divideAndCount(self.invalidTrainData)
		self.validWordsTotal, self.validWordsCountTable = self.divideAndCount(self.validTrainData)

		# self.ps = float(self.invalidWordsTotal)/(self.invalidWordsTotal + self.validWordsTotal)
		# self.ph = float(self.validWordsTotal)/(self.invalidWordsTotal + self.validWordsTotal)
		self.ps = configure.BayesianSetting[bayesType + "_ps"]
		self.ph = configure.BayesianSetting[bayesType + "_ph"]
		print "invalidWordsTotal", self.invalidWordsTotal
		print "validWordsTotal", self.validWordsTotal
		print "ps", self.ps
		print "ph", self.ph

		self.train()
		fileProbabilityTable = file("../data/nameWordProbabilityTable.dat", "w")
		cPickle.dump(self.wordProbabilityTable, fileProbabilityTable)
		print "Dump successfully!"
		
	'''用于分割训练数据, 并得到各个单词的词频'''
	def divideAndCount(self, lines):
		words = {}
		Total = 0
		for line in lines:
			# 利用jieba分词,获取每个训练数据的最有说服力的topk数据, 
			# 并筛选stopwords
			# tags = list(jieba.analyse.extract_tags(line,topK = 2))
			tags = list(jieba.cut(line, cut_all=0))
			for word in tags:
				if word.encode("utf-8") not in self.stopwordList:
					Total +=1
					if words.has_key(word):
						words[word] += 1
					else:
						words[word] = 1
		return Total, words
	

	'''训练函数 得出词语概率表'''
	def train(self):
		# used to stored p(s|w)
		self.wordProbabilityTable = {}
		# 计算出出现在invalidWordsCountTable 的词语的p(s|w)
		for word in self.invalidWordsCountTable:
			# s_tmpP = p(w|s)*ps
			s_tmpP = float(self.invalidWordsCountTable[word] + laplaceValue)/self.invalidWordsTotal*self.ps
			#h_tmpP = p(w|h)*ph
			if word in self.validWordsCountTable:
				h_tmpP = float(self.validWordsCountTable[word]+laplaceValue)/self.validWordsTotal*self.ph
			else:
				h_tmpP = float(laplaceValue)/self.validWordsTotal*self.ph

			# p(s|w) = p(w|s)*ps/ (p(w|s)*ps + p(w|h)*ph)
			word_p = s_tmpP/(s_tmpP + h_tmpP)
			self.wordProbabilityTable[word] = word_p

		for word in self.validWordsCountTable:
			if not word in self.wordProbabilityTable:
				h_tmpP = float(self.validWordsCountTable[word]+laplaceValue)/self.validWordsTotal*self.ph
				s_tmpP = float(laplaceValue)/self.invalidWordsTotal*self.ps
				word_p = s_tmpP/(s_tmpP + h_tmpP)
				self.wordProbabilityTable[word] = word_p
				
	'''测试函数'''
	def test(self):
		fileptr = file("../debugInfo/tmprecord", "w")
		probablitylist = sorted(self.wordProbabilityTable.items(), key=lambda d:d[1])
		for i in probablitylist:
			fileptr.write(i[0].encode("utf-8") + " " + str(i[1]) + "\n")
			# print i[0].encode("utf-8"), i[1]


if __name__=="__main__":
	fileptr = file("../data/invalidName.dat.new", "r")
	# fileptr = file("info3/invalidDescription.dat.new", "r")
	fileptr1 = file("../data/validName.dat.new", "r")
	# fileptr1 = file("info3/validDescription.dat.new", "r")
	invalidLines = fileptr.readlines()
	invalidLines = [line.rstrip() for line in invalidLines]
	validLines = fileptr1.readlines()
	validLines = [line.rstrip() for line in validLines]
	fiter = bayesTrain(validLines, invalidLines, "name")
