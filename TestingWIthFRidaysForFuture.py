import http.client
import json
import datetime
import facebook
from datetime import timezone
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

def getDifferentPhotoURL(id):
	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }
	conn.request("GET", "/wp-json/wp/v2/media/"+str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	photoURL={
		"actual_size":data["media_details"]["sizes"]["full"]["source_url"],
	"default":data["media_details"]["sizes"]["sow-carousel-default"]["source_url"],
	"thumbnail":data["media_details"]["sizes"]["thumbnail"]["source_url"]}
	#"medium":data[0]["media_details"]["sizes"]["medium"]["source_url"],
	try:
		photoURL.add("medium",data["media_details"]["sizes"]["medium"]["source_url"])
	except:
		print("Medium size doesn't exist")
	try:
		photoURL.add("medium_large",data["media_details"]["sizes"]["medium"]["medium_large"])
	except:
		print("Medium Large size doesn't exist")

	return photoURL

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

	conn.request("GET", "/wp-json/wp/v2/tags?post="+str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	tags1 = ""
	for i in data:
		tag1 = i["name"].replace(" ", "")
		tag1 = tag1.replace("-", "_")            
		tags1 += "#"+tag1+" "
	print (tags1)
	return (tags1)

def publishArticle(mess,ti,url,murl,pageID,accesst):
	graph = facebook.GraphAPI(access_token=accesst)
	b=pageID
	tim=str(int(ti))
	print(url)
	a= graph.put_object(
	parent_object=str(b),
	connection_name="feed",
	published="false",
	message=str(mess),
	scheduled_publish_time=tim,
	link=url,
	is_hidden="false",
	#attachments={"media":{"image":murl}})
	attachment =  {
		"name": str(murl),
		"link": url,
		"caption": 'Check out this example',
		"description": "This is a longer description of the attachment",
		"picture": murl})
	print (a)

	"""
	try:
		a= graph.put_object(
			parent_object=str(b),
			connection_name="feed",
			published="false",
			message=str(mess),
			scheduled_publish_time=tim,
			link=url,
			is_hidden="false",
			#attachments={"media":{"image":murl}})
			attachment =  {
        "name": str(murl),
        "link": url,
        "caption": 'Check out this example',
        "description": "This is a longer description of the attachment",
        "picture": murl})
		print (a)
	except:
		print("There is some error")
		time.sleep(20)
		publishArticle(mess,ti,url,murl,accesst,pageID)
		"""
	return a 

def publishPhotoArticle(mess,ti,murl,accesst,pageID):
	graph = facebook.GraphAPI(access_token=accesst)
	b=pageID
	tim=str(int(ti))
	a= graph.put_object(
	parent_object=str(b),
	connection_name="photos",
	is_hidden="false",
	published="false",
	url = murl,
	message=mess,
	scheduled_publish_time=tim,
	full_picture=murl)
	print (a)
	return a 

def getArticleAttachment(id1,accesst):
	graph = facebook.GraphAPI(access_token=accesst)
	a= graph.get_object(
		id=id1,
		fields=("message","attachments{media}")) 
	return a

def getArticleAttachmentForPhoto(id1,accesst):
	graph = facebook.GraphAPI(access_token=accesst)
	a= graph.get_object(
		id=id1,
		fields=("message","images")) 
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
issueDate = datetime.datetime(2020,7,26).date()

elevenAM= datetime.datetime(2020, 8, 10,5,40)
threePM = datetime.datetime(2020, 8, 10,9,30)
sixPM = datetime.datetime(2020, 8, 10,12,30)
nineAM = datetime.datetime(2020, 8, 10,4)

currentTime = int(x.replace(tzinfo=timezone.utc).timestamp()) 
currentTime = currentTime-19080
elevenAM = elevenAM.replace(tzinfo=timezone.utc).timestamp()
threePM = threePM.replace(tzinfo=timezone.utc).timestamp()
sixPM = sixPM.replace(tzinfo=timezone.utc).timestamp()
nineAM = nineAM.replace(tzinfo=timezone.utc).timestamp()

access_token="EAAYY9ZBJvM0QBAFWCsuWZB2gfGJ7S18M4K36glfDxgfRRbZBouoUr4CG2PIGDVtZA9TptNnvboT2dyVhFF6bZCKMbyetjEdhOpZCsM4TV2Y0JIXTwHeENOXQTUBVJTCuP1AxxXCUqvbe1wjQLdD46bQXrkUlpCX2oteoTageOrzuX6J5pPYbe61fEIDZAeJXNcM0CpnqFHvCkgOb1xpMl390c6L8OktvhMZD"
pageID = 319140888763658
#108144264067982
#319140888763658

for i in range(29,-1,-1):
	currentIssueDate = datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()
	if (issueDate == currentIssueDate):
		print(getAuthorName(data[i]["author"]))
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
		strF1 += getTags(data[i]["id"])
		link = data[i]["link"]
		photoId  = data[i]["featured_media"]
		murl = getDifferentPhotoURL(photoId)
		currentID=publishArticle(strF1,eachPostTime[i],link,murl["actual_size"],pageID,access_token)
		attachMent = getArticleAttachment(currentID["id"],access_token)
		attachmentName = "attachments"
		graph = facebook.GraphAPI(access_token=access_token)

		if attachmentName in attachMent:
			print("Attachment exists")
		else:
			
			delete1=graph.delete_object(currentID["id"])
			print("Attachment doesn't exist for article hence publishing smaller image. Delete status:",delete1)
			currentID=publishArticle (strF1,eachPostTime[i],link,murl["default"],pageID,access_token)

			attachMent = getArticleAttachment(currentID["id"],access_token)

			if attachmentName in attachMent:
				print("Attachment exists")
			else:
				delete1=graph.delete_object(currentID["id"])
				print("Attachment doesn't exist for article hence publishing photo article. Delete status:",delete1)
				currentID=publishPhotoArticle(strF1,eachPostTime[i],murl["actual_size"],access_token,pageID)

				attachMent = getArticleAttachmentForPhoto(currentID["id"],access_token)
				attachmentName = "images"
				if attachmentName in attachMent:
					print("Attachment exists")
				else:
					print("No method works, must do manually",)

		id.append(currentID)
		uday="rockes"
	j=j+1

q=0
while (q<len(id)):
	graph = facebook.GraphAPI(access_token=access_token)
	graph.delete_object(id[q]["id"])
uday =1

#1592199000 means post will get scheduled at 11am
#Check this link to get time in above format: (https://www.unixtimestamp.com/index.php)
#Also note that, the fb time is 5:30 hours more.So if post is scheduled at 2 am post is scheduled at 7:30 pm. But this condition is covered in given above code.
#24 hours = 86400 seconds
# 1 houre = 3600 seconds