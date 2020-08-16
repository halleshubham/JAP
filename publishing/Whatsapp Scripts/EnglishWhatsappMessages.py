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

def removeUnwantedtext(id):
	id = id.replace("&#8217","'")
	id = id.replace("&#8220","“")
	id = id.replace("&#8221","'")
	id = id.replace("&#8217","'")
	return id
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
imp = "-----------------------------------------------------------\n 📱 _Join Lokayat's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/DxY7U42lGBeHyLJwUYCtn4\n\n"
imp += "📱 _लोकायतचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/DQtYRIIuydR2fMTjTHVcOT\n\n"
imp += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"
j=0
i=l
strF1=""
while j<7:
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		strF1 += "⭕ *"+data[i]["title"]["rendered"]+"*\n\n"
		authorName = getAuthorName(data[i]["author"]) 
		excerpt = data[i]["excerpt"]["rendered"]
		excerpt = excerpt.rstrip("\n")
		excerpt = excerpt.replace("<p>", "")
		excerpt = excerpt.replace("</p>", "")
		excerpt = removeUnwantedtext(excerpt)
		strF1 += "✒️ "+authorName+"\n\n_"+excerpt+"_\n\n*Read full article:*\n"
		strF1 += data[i]["link"]+"\n\n"+imp
		j=j+1
	i=i-1
print (strF1)

f3 = open("EnglishWhatsappMessages.txt","w",encoding="UTF-8")
f3.write(strF1)
f3.close()