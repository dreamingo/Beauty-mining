import re
import configure
import weiboComment
from bayesFilter import bayesFilter as bayesFilter

class isbeauty():
	def __init__(self):
		self.commmentFilter = bayesFilter("comment") 
		self.validfileptr = file("../debugInfo//validComment", "a")
		self.invalidfileptr = file("../debugInfo/invalidComment", "a")

	def judge(self, eachTimeline, client):
		Get_sum = 0;
		comments_count = eachTimeline["comments_count"]
		reposts_count = eachTimeline["reposts_count"]

		if reposts_count !=0:
			Get_sum  += comments_count/reposts_count
		else:
			Get_sum += comments_count

		# allComments = client.get.comments__show(id=eachTimeline["id"])
		allComments = weiboComment.getComment(eachTimeline["mid"], eachTimeline["user"]["id"])
		for eachComment in allComments:
			if not self.commmentFilter.myFilter(eachComment):
				print "++++++++++++++++++++++++++++++++++++"
				print eachComment.decode("utf-8") 
				self.validfileptr.write(eachComment + "\n")
				Get_sum += 15
			else:
				self.invalidfileptr.write(eachComment + "\n")

		if Get_sum > 25:
			return True
