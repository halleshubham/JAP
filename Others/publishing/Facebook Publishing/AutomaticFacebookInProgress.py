import requests
import http.client
import json
import datetime
import re
import facebook
from datetime import timezone
import sys

def getAuthorName(id):
	conn = http.client.HTTPConnection("janataweekly.org")

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
	conn = http.client.HTTPConnection("janataweekly.org")

	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }
	conn.request("GET", "/wp-json/wp/v2/tags/"+str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	print(data["name"]) 
	return data["name"]

def publishArticle(mess,time,url):
	try:
		graph = facebook.GraphAPI(access_token="EAAYY9ZBJvM0QBAPV04DmzbG84LrSG7ziZA234NAoBxoZAHwkJhNwgNBK71gFPvmZBQvZCFjgcRKrkOAby2jZAKUz5qo6vZA360ZB5BZB0lUyLDN2gZAuaFVNvzOTbYbMWKfD1ReOCuqg9Vy2XxNb0Q5aM8Fz59ogfLMhSZC1CJjfuWq5VGadzZCT4qsQJ8tZAdZBZAAyxRhw6gs0q6fTQZDZD")
		b=319140888763658
		time=str(int(time))
		print(url)
		a= graph.put_object(
		   parent_object=str(b),
		   connection_name="feed",
		   published="false",
		   message=str(mess),
		   scheduled_publish_time=time,
		   link=url)
		print (a)
	except:
		print("Oops!", sys.exc_info()[0], "occurred.")
		print("Next entry.")
		print()

conn = http.client.HTTPConnection("janataweekly.org")

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

conn.request("GET", "/wp-json/wp/v2/posts?per_page=36")
res = conn.getresponse()
data = json.loads(res.read())

refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')
l=0

for i in range(29,-1,-1):
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		l=l+1

j=21
x = datetime.datetime.now()
elevenAM= datetime.datetime(2020, 6, 24,5,30)
threePM = datetime.datetime(2020, 6, 24,9,30)
sixPM = datetime.datetime(2020, 6, 24,12,30)
nineAM = datetime.datetime(2020, 6, 24,4)

elevenAM = elevenAM.replace(tzinfo=timezone.utc).timestamp()
threePM = threePM.replace(tzinfo=timezone.utc).timestamp()
sixPM = sixPM.replace(tzinfo=timezone.utc).timestamp()
nineAM = nineAM.replace(tzinfo=timezone.utc).timestamp()

while j<l:
	if (refDateObj.date() - datetime.datetime.strptime(data[l-j]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		strF1 = data[l-j]["title"]["rendered"]+"\n\n"
		authorName = getAuthorName(data[l-j]["author"]) 
		excerpt = data[l-j]["excerpt"]["rendered"]
		excerpt = excerpt.rstrip("\n")
		excerpt = excerpt.replace("<p>", "")
		excerpt = excerpt.replace("</p>", "")
		excerpt = removeUnwantedtext(excerpt)
		strF1 += authorName+"\n\n"+excerpt+"\n\n"
		link = data[l-j]["link"]
		strF1 += link +"\n\n"
		a = len(data[l-j]["tags"])
		for s in range(1,a,1):	                
			tag = getTags(data[l-j]["tags"][s])
			tag = tag.replace(" ", "")
			tag = tag.replace("-", "_")            
			strF1 += "#"+tag+" "
			print(tag)
		if (j<7):
			publishArticle (strF1,elevenAM,link)
			elevenAM += 86400
		elif (j>=7 and j<14):
			publishArticle (strF1,threePM,link)
			threePM += 86400
		elif (j>=14 and j<21):
			publishArticle (strF1,sixPM,link)
			sixPM += 86400
		else:
			publishArticle(strF1,nineAM,link)			
			nineAM += 86400
		j=j+1

uday =1

#1592199000 means post will get scheduled at 11am
#Check this link to get time in above format: (https://www.unixtimestamp.com/index.php)
#Also note that, the fb time is 5:30 hours more.So if post is scheduled at 2 am post is scheduled at 7:30 pm. But this condition is covered in given above code.
#24 hours = 86400 seconds
# 1 houre = 3600 seconds