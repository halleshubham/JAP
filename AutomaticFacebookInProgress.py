import requests
import http.client
import json
import datetime
import re
import facebook
from datetime import timezone
import sys
import time

def getAuthorName(id):
	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }

	conn.request("GET", "/wp-json/wp/v2/users/"+str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	return data["name"]

def removeUnwantedtext(id):
	id = id.replace("&#8217","'")
	id = id.replace("&#8220","“")
	id = id.replace("&#8221","'")
	id = id.replace("&#8217","'")
	return id

def getTags(id):
	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }
	conn.request("GET", "/wp-json/wp/v2/tags/"+str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	print(data["name"]) 
	return data["name"]

def publishArticle(mess,ti,url,murl):
	graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBAHGGXm8sRiquTu91wsG6zdXfZBZAfn7CAMPXIP89EqxJ2Cjmj0N2AaZBpvUO0zKp6E7R1cKgjZCCERL8ELI2ZBgzGxTBFizSqufw41JmYokg0PN77Ridj50PFy1QNJLPZCFawKwjvJYZB2e549vqYLvZCRwUAxGbPB7TwOvOEGZCNpGp6eaFLT18z3LxC9ZCZBZAdQZDZD")
	b=319140888763658
	tim=str(int(ti))
	print(url)
	try:
		a= graph.put_object(
			parent_object=str(b),
			connection_name="feed",
			published="false",
			message=str(mess),
			scheduled_publish_time=tim,
			is_hidden="false",
			link=url,
			full_picture=murl,
			attachments={"media":{"image":murl}})
		print (a)
	except:
		print("There is some error")
		time.sleep(20)
		publishArticle(mess,ti,url,murl)
	return a 

def getArticleAttachment(id1):
	graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBAHGGXm8sRiquTu91wsG6zdXfZBZAfn7CAMPXIP89EqxJ2Cjmj0N2AaZBpvUO0zKp6E7R1cKgjZCCERL8ELI2ZBgzGxTBFizSqufw41JmYokg0PN77Ridj50PFy1QNJLPZCFawKwjvJYZB2e549vqYLvZCRwUAxGbPB7TwOvOEGZCNpGp6eaFLT18z3LxC9ZCZBZAdQZDZD")
	a= graph.get_object(
		id=id1,
		fields=("message","attachments{media}")) 
	return a

conn = http.client.HTTPSConnection("janataweekly.org")

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

conn.request("GET", "/wp-json/wp/v2/posts?per_page=30")
res = conn.getresponse()
data = json.loads(res.read())

l=0
eachPostTime = {}

x = datetime.datetime.now()
todayDate = x.date()
issueDate = datetime.datetime(2020,6,21).date()

elevenAM= datetime.datetime(2020, 6, 29,5,40)
threePM = datetime.datetime(2020, 6, 29,9,30)
sixPM = datetime.datetime(2020, 6, 29,12,30)
nineAM = datetime.datetime(2020, 6, 29,4)

currentTime = int(x.replace(tzinfo=timezone.utc).timestamp()) 
currentTime = currentTime-19080
elevenAM = elevenAM.replace(tzinfo=timezone.utc).timestamp()
threePM = threePM.replace(tzinfo=timezone.utc).timestamp()
sixPM = sixPM.replace(tzinfo=timezone.utc).timestamp()
nineAM = nineAM.replace(tzinfo=timezone.utc).timestamp()

for i in range(29,-1,-1):
	print(getAuthorName(data[i]["author"]))
	currentIssueDate = datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()
	if (issueDate == currentIssueDate):
		if (l<7):
			eachPostTime[i]=elevenAM
			elevenAM += 86400
		elif (l>=7 and l<14):
			eachPostTime[i]=threePM
			threePM += 86400
		elif (l>=14 and l<21):
			eachPostTime[i]=sixPM
			sixPM += 86400
		else:		
			eachPostTime[i]=nineAM
			nineAM += 86400
		l=l+1

j=0

id =[]

for i in range(l-1,-1,-1):
	print(getAuthorName(data[i]["author"]))
	if (eachPostTime[i]>currentTime):
		strF1 = data[i]["title"]["rendered"]+"\n\n"
		authorName = getAuthorName(data[i]["author"]) 
		excerpt = data[i]["excerpt"]["rendered"]
		excerpt = excerpt.rstrip("\n")
		excerpt = excerpt.replace("<p>", "")
		excerpt = excerpt.replace("</p>", "")
		excerpt = removeUnwantedtext(excerpt)
		strF1 += authorName+"\n\n"+excerpt+"\n\n"
		strF1 += data[i]["link"] +"\n\n"
		a = len(data[i]["tags"])
		for j in range(1,a,1):	                
			tag = getTags(data[i]["tags"][j])
			tag = tag.replace(" ", "")
			tag = tag.replace("-", "_")            
			strF1 += "#"+tag+" "
			print(tag)
		link = data[i]["link"]
		murl = data[i]["jetpack_featured_media_url"]
		currentID=(publishArticle (strF1,eachPostTime[i],link,murl))
		attachMent = getArticleAttachment(currentID["id"])
		attachmentName = "attachments"
		graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBAHGGXm8sRiquTu91wsG6zdXfZBZAfn7CAMPXIP89EqxJ2Cjmj0N2AaZBpvUO0zKp6E7R1cKgjZCCERL8ELI2ZBgzGxTBFizSqufw41JmYokg0PN77Ridj50PFy1QNJLPZCFawKwjvJYZB2e549vqYLvZCRwUAxGbPB7TwOvOEGZCNpGp6eaFLT18z3LxC9ZCZBZAdQZDZD")

		if attachmentName in attachMent:
			print("Attachment exists")
		else:
			print("Attachment doesn't exist")
			id.append(currentID)
		uday="rockes"
	j=j+1

q=0
while (q>=len(id)):
	graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBAHGGXm8sRiquTu91wsG6zdXfZBZAfn7CAMPXIP89EqxJ2Cjmj0N2AaZBpvUO0zKp6E7R1cKgjZCCERL8ELI2ZBgzGxTBFizSqufw41JmYokg0PN77Ridj50PFy1QNJLPZCFawKwjvJYZB2e549vqYLvZCRwUAxGbPB7TwOvOEGZCNpGp6eaFLT18z3LxC9ZCZBZAdQZDZD")
	graph.delete_object(id["id"][q])
uday =1

#1592199000 means post will get scheduled at 11am
#Check this link to get time in above format: (https://www.unixtimestamp.com/index.php)
#Also note that, the fb time is 5:30 hours more.So if post is scheduled at 2 am post is scheduled at 7:30 pm. But this condition is covered in given above code.
#24 hours = 86400 seconds
# 1 houre = 3600 seconds