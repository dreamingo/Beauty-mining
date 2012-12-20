Weibo beauty Mining 
=============================

Just For Fun.Mining the beauty who are within n weibo relationship with you and download all of their self-portraits shots 

This is a pure Python Program, dependencies are shown below

Notoice
---------------
I strongly recommend you should read this README and other dataFile of  this project in linux, or in encoding UTF-8, not windows GBK


Dependencies
------------

* Linux Platform(Ubuntu 12.04)
* Python2.7 (Python3 is not supported)
* python-bs4
* python-htmllib5
* jieba

Installation
-------------
Use the following command to install python libraries
	sudo apt-get install python-bs4
	sudo apt-get install python-htmllib5
	sudo apt-get install pip
	sudo pip install jieba


Resource files
----------------
The file structure are shown below

	AIproject/
	│
	├── data/								#use to store the bayesian data
	│   ├── .........
	│   ├── trainData/						#use to store the bayesian traning data
	│   │   ├── .......
	│ 
	├── debugInfo/							#Use to recorde the Info when program was running
	│ 
	├── img/								#The result--Beauty img(TA welfare!!!)
	│ 
	└── src
		├── analysis.py						#Anaylsis model
		├── base62.py						#use to caculate the encryption key of tweetconet when crawling
		├── bayesFilter.py					#Use to classify a text
		├── bayesTrain.py					#Use to train the bayesian filter
		├── configure.py					#use to store all the configure setting of the project
		├── isbeauty.py						#Use to	judge a node's pic is a beauty or not
		├── login.py						#weiboAPI login and crawler login
		├── main.py
		├── searchNode.py					#Defination of the searchNode
		├── Search.py						#SearchModel
		├── weiboComment.py					#The crawler use to craw assignated tweet's comment
		└── weibo.py						#WeibAPI SDK
Usage
-------

First of all, After installing all the dependencies, 
Since our project get data from both weiboAPI and crawler, you should modified the configure.py first
```
	APP_KEY = "YOUR APP_KEY"
	APP_SECRET = "YOUR_APP_SECRET"
	CALLBACK_URL = ""
	ACCOUNT = "YOUR WEIBO ACCOUNT"
	PASSWORD = "YOUR WEIBO PASSWORD"
```

Since the limit of the API use, we strongly recomment you should run the "Search model" & "Analasis model" seperatily
After run main.py, you will get the following choice:

```
	1.Run the Search Model
	2.Run the Analysis Model
```
If you want to run the Search model, Please select 1, otherwiese please select 2
(After running the Search Model you'd better reboot the program and choice 2 to run Anlasis model)

Since the work amount and data was so huge, it take a long time for this project to run
```
	The search model may cost 45min
	the Analysis Model(included img download), may cause 8 hours to download the top 50 beauty's self-portraits shots
```

Todo
------
1. More explicit search range
User can narrow down the search range as they want. such as they can restrict the target was graduated from SYSU and so on.

2. Not just focus on beauty.The user can define their own key words to get the niceness around them such as love pets, handsome boy, beautiful scenery and so on.

