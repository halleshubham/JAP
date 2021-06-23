import http.client
import json
import datetime
import re
import unicodedata

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

def AbhivyaktiAndLokayatEnglishWhatsAppMessages(numberOfArticles):
	conn = http.client.HTTPSConnection("janataweekly.org")

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

	lokayatFooter = "-----------------------------------------------------------\n 📱 _Join Lokayat's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/GZfbm0OcsTN5OfOsnoUGBU\n\n"
	lokayatFooter += "📱 _लोकायतचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/Gr322B7eE5f7dUCQfcbv5O\n\n"
	lokayatFooter += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"

	abhivyaktiFooter = "-----------------------------------------------------------\n 📱 _Join Abhivyakti's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/IYdOYT4MuCtDNhkgHoVKn0\n\n"
	abhivyaktiFooter += "📱 _अभिव्यक्तीचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/Dvrwcdpw0TdDYMsRciyufS\n\n"
	abhivyaktiFooter += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"
	j=0
	i=l
	strF1=""
	strAbhivyakti =""

	while j<numberOfArticles:
		if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:

			title = data[i]["title"]["rendered"]
			titleEnd =  [-1]
			titleStart = title[0]
			if (titleEnd == ' '):
				title = title[:-1]
			if (titleStart == ' '):
				title = title[1:]

			strF1 += "⭕ *"+title+"*\n\n"
			strAbhivyakti += "⭕ *"+title+"*\n\n"

			authorName = getAuthorName(data[i]["author"]) 
			excerpt = data[i]["excerpt"]["rendered"]

			excerpt2 = unicodedata.normalize("NFKD",excerpt)

			excerpt = excerpt.rstrip("\n")
			excerpt = excerpt.replace("<p>", "")
			excerpt = excerpt.replace("</p>", "")
			excerpt = removeUnwantedtext(excerpt)

			authorStart= authorName[0]
			authorEnd= authorName[-1]
			if (authorEnd == ' '):
				authorName = authorName[:-1]
			if (authorStart == ' '):
				authorName = authorName[1:]
				
			excerptStart= excerpt[0]
			excerptEnd= excerpt[-1]
			if (excerptEnd == ' '):
				excerpt = excerpt[:-1]
			if (excerptStart == ' '):
				excerpt = excerpt[1:]

			a= excerpt[-1]
			if (a == ' '):
				excerpt = excerpt.replace(" ", "")

			strF1 += "✒️ "+authorName+"\n\n_"+excerpt+"_\n\n*Read full article:*\n"
			strAbhivyakti += "✒️ "+authorName+"\n\n_"+excerpt+"_\n\n*Read full article:*\n"

			strAbhivyakti += data[i]["link"]+"\n\n"+abhivyaktiFooter
			strF1 += data[i]["link"]+"\n\n"+lokayatFooter
		
			j=j+1
		i=i-1
	print (strF1)

	f3 = open("EnglishWhatsappMessagesWithLokayatFooter.txt","w",encoding="UTF-8")
	f3.write(strF1)
	f3.close()

	f4 = open("EnglishWhatsappMessagesWithAbhivyaktiFooter.txt","w",encoding="UTF-8")
	f4.write(strAbhivyakti)
	f4.close()

AbhivyaktiAndLokayatEnglishWhatsAppMessages(28)