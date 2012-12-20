import cPickle

def analysis(client):
	searchNodeptr = file("../debugInfo/UserlistPickle", "r")
	AllNodes = cPickle.load(searchNodeptr)

	count = 1
	errorInfoRecord = file("../debugInfo/errorInfoRecord", "w")
	for i in range(2, 100):
		print "======================================================="
		print str(count) + ": Getting " + AllNodes[i].getName() + " statuses!"
		AllNodes[i].getStatuses(client,i, errorInfoRecord)
		count +=1





