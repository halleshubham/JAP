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
	photoURL = {}

	try:
		photoURL["medium"] = data["media_details"]["sizes"]["medium"]["source_url"]
	except:
		print("Medium size doesn't exist")

	try:
		photoURL["thumbnail"] = data["media_details"]["sizes"]["woocommerce_thumbnail"]["source_url"]
	except:
		print("woocommerce_thumbnail size doesn't exist")

	try:
		photoURL["default"] = data["media_details"]["sizes"]["woocommerce_gallery_thumbnail"]["source_url"]
	except:
		print("woocommerce_gallery_thumbnail size doesn't exist")

	try:
		photoURL["actual_size"] = data["media_details"]["sizes"]["full"]["source_url"]
	except:
		print("full size doesn't exist")

	try:
		photoURL["medium_large"] = data["media_details"]["sizes"]["medium"]["medium_large"]
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

def publishingAllArticles(dates,pageID,access_token,summary,postsTobeDeleted):
	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache"
		}

	conn.request("GET", "/wp-json/wp/v2/posts?per_page=30")
	res = conn.getresponse()
	data = json.loads(res.read())

	eachPostTime = {}

	x = datetime.datetime.now()
	todayDate = x.date()
	issueDate = datetime.datetime(dates["current_issue_Date"][0],dates["current_issue_Date"][1],dates["current_issue_Date"][2]).date()

	elevenAM= datetime.datetime(dates["date_For_First_Seven_Articles"][0], dates["date_For_First_Seven_Articles"][1], dates["date_For_First_Seven_Articles"][2],dates["date_For_First_Seven_Articles"][3],dates["date_For_First_Seven_Articles"][4])
	threePM = datetime.datetime(dates["date_For_Seven_To_Fourteen_Articles"][0], dates["date_For_Seven_To_Fourteen_Articles"][1], dates["date_For_Seven_To_Fourteen_Articles"][2],dates["date_For_Seven_To_Fourteen_Articles"][3],dates["date_For_First_Seven_Articles"][4])
	sixPM = datetime.datetime(dates["date_For_Fourteen_To_TwentyOne_Articles"][0], dates["date_For_Fourteen_To_TwentyOne_Articles"][1], dates["date_For_Fourteen_To_TwentyOne_Articles"][2],dates["date_For_Fourteen_To_TwentyOne_Articles"][3],dates["date_For_Fourteen_To_TwentyOne_Articles"][4])
	nineAM = datetime.datetime(dates["date_For_TwentyOne_To_Further_Articles"][0], dates["date_For_TwentyOne_To_Further_Articles"][1], dates["date_For_TwentyOne_To_Further_Articles"][2],dates["date_For_TwentyOne_To_Further_Articles"][3])

	currentTime = int(x.replace(tzinfo=timezone.utc).timestamp()) 
	currentTime = currentTime-19080
	elevenAM = elevenAM.replace(tzinfo=timezone.utc).timestamp()
	threePM = threePM.replace(tzinfo=timezone.utc).timestamp()
	sixPM = sixPM.replace(tzinfo=timezone.utc).timestamp()
	nineAM = nineAM.replace(tzinfo=timezone.utc).timestamp()

	access_token=access_token
	pageID = 319140888763658
	#108144264067982
	#319140888763658

	author= summary[0]['authors']
	excerpt=summary[0]['excerpts']
	title=summary[0]['titles']
	l=len(author)
	if (l >29):
		l = 29
	for i in range(0,l):
		currentIssueDate = datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()
		#for reverse replace i with l-i-1
		if (issueDate == currentIssueDate):
			if ((l-i)<7):
				eachPostTime[i]=elevenAM
				elevenAM += 86400
			elif ((l-i)>=7 and (l-i)<14):
				eachPostTime[i]=threePM
				threePM += 86400
			elif ((l-i)>=14 and (l-i)<21):
				eachPostTime[i]=sixPM
				sixPM += 86400
			else:		
				eachPostTime[i]=nineAM
				nineAM += 86400
		else:
			print ("UDy")

	j=0

	id =[]
	author= summary[0]['authors']
	excerpt=summary[0]['excerpts']
	title=summary[0]['titles']
#for reverse replace range(l-1,-1,-1) with range(0,l)
	for i in range(0,l):
		print(author[i])
		if (eachPostTime[i]>currentTime):
			#for reverse replace i with l-i-1
			strF1 = title[i]+"\n\n"
			strF1 += author[i]+"\n\n"+excerpt[i]+"\n\n"
			strF1 += data[i]["link"] +"\n\n"
			strF1 += getTags(data[i]["id"])
			link = data[i]["link"]
			photoId  = data[i]["featured_media"]
			murl = getDifferentPhotoURL(photoId)
			print (strF1,"\n")
			currentID = publishArticle(strF1,eachPostTime[i],link,murl["actual_size"],pageID,access_token)
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
			uday="rocks"
		j=j+1

	q=0
	if (postsTobeDeleted == "true"):
		while (q<len(id)):
			graph = facebook.GraphAPI(access_token=access_token)
			graph.delete_object(id[q]["id"])
			q += 1
		uday =1

#1592199000 means post will get scheduled at 11am
#Check this link to get time in above format: (https://www.unixtimestamp.com/index.php)
#Also note that, the fb time is 5:30 hours more.So if post is scheduled at 2 am post is scheduled at 7:30 pm. But this condition is covered in given above code.
#24 hours = 86400 seconds
# 1 houre = 3600 seconds