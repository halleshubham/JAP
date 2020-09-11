import http.client
import json
import datetime
import re


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

conn = http.client.HTTPSConnection("janataweekly.org")

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

conn.request("GET", "/wp-json/wp/v2/posts?per_page=30")
res = conn.getresponse()
data = json.loads(res.read())

refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')
strF = '\nArticles for this week\n\n'
k=1
for i in range(29,-1,-1):
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		strF +=  str(k)+"\n\n"+data[i]["title"]["rendered"]+"\n"
		k=k+1
		authorName = getAuthorName(data[i]["author"])
		excerpt = data[i]["excerpt"]["rendered"]
		excerpt = excerpt.replace("<p>", "")
		excerpt = excerpt.replace("</p>", "")
		a = len(data[i]["tags"])
		strF += "\nBy "+authorName+"\n\n"+excerpt+"\n"
		tags = getTags(data[i]["id"])
		# strF += "By _AuthorName_\n"
		strF +=  data[i]["link"] + "\n\n"+tags+"\n\n\n"
		# data[i]["jetpack_featured_media_url"] 

print(strF)
f = open("facebook.txt","w",encoding="UTF-8")
f.write(strF)
f.close()

