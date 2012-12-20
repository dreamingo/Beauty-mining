#coding=utf-8
import login
import Search
import json
import analysis
if __name__ == '__main__':
	client = login.APILogin()
	login.browserLogin()
	print "========================="
	print "1.Run the Search Model"
	print "2.Run the Analysis Model"
	choice = int(raw_input("Your choice:"))
	if choice == 1:
		Search.search(client)
	elif choice == 2:
		analysis.analysis(client)
	else:
		print "Invalid choice!"
	
