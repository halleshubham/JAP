import http.client
import json
import datetime
import re


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

conn = http.client.HTTPConnection("janataweekly.org")

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
		strF +=  str(k)+"\n"+data[i]["title"]["rendered"]+"\n"
		k=k+1
		authorName = getAuthorName(data[i]["author"])
		excerpt = data[i]["excerpt"]["rendered"]
		excerpt = excerpt.replace("<p>", "")
		excerpt = excerpt.replace("</p>", "")
		a = len(data[i]["tags"])
		strF += "\nBy "+authorName+"\n\n"+excerpt+"\n\n"
		for j in range(1,a,1):	                
			tag = getTags(data[i]["tags"][j])
			tag = tag.replace(" ", "")
			tag = tag.replace("-", "_")            
			strF += "#"+tag+" "
			print(tag)
		# strF += "By _AuthorName_\n"
		strF += "\n\n"+data[i]["link"]
		# data[i]["jetpack_featured_media_url"] 

print(strF)
f = open("facebook.txt","w",encoding="UTF-8")
f.write(strF)
f.close()

