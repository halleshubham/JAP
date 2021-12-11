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

def AbhivyaktiAndLokayatEnglishWhatsAppMessages(summary):

	author= summary[0]['authors']
	excerpt=summary[0]['excerpts']
	title=summary[0]['titles']

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

	lokayatFooter = "-----------------------------------------------------------\n 📱 _Join Lokayat's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/E8EjevJvIyN8q3LourelZP\n\n"
	lokayatFooter += "📱 _लोकायतचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/L9EA1WMO0Xh2PK5sD5mgGQ\n\n"
	lokayatFooter += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"

	abhivyaktiFooter = "-----------------------------------------------------------\n 📱 _Join Abhivyakti's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/IYdOYT4MuCtDNhkgHoVKn0\n\n"
	abhivyaktiFooter += "📱 _अभिव्यक्तीचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/Cc2Mf0iD5728O1Kr7byL7H\n\n"
	abhivyaktiFooter += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"
	j=0
	i=l
	strF1=""
	strAbhivyakti =""

	while j<len(author):
		if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:

			title[i] = unicodedata.normalize("NFKD",title[i])
			author[i] = unicodedata.normalize("NFKD",author[i])
			excerpt[i] = unicodedata.normalize("NFKD",excerpt[i])

			if (author[i].__contains__('\t')):
				author[i] = author[i].replace("\t", "", -1)

			if (title[i].__contains__('\t')):
				title[i] = title[i].replace("\t", "", -1)

			if (excerpt[i].__contains__('\t')):
				excerpt[i] = excerpt[i].replace("\t", "", -1)

			authorStart= author[i][0]
			while (authorStart == ' '):
				author[i] = author[i][1:]
				authorStart= author[i][0]

			authorEnd= author[i][-1]
			while (authorEnd == ' '):
				author[i] = author[i][:-1]
				authorEnd= author[i][-1]
				
			excerptStart= excerpt[i][0]
			while (excerptStart == ' '):
				excerpt[i] = excerpt[i][1:]
				excerptStart= excerpt[i][0]

			excerptEnd= excerpt[i][-1]
			while (excerptEnd == ' '):
				excerpt[i] = excerpt[i][:-1]
				excerptEnd= excerpt[i][-1]
				
			titleStart = title[i][0]
			while (titleStart == ' '):
				title[i] = title[i][1:]
				titleStart = title[i][0]

			titleEnd = title[i][-1]
			while (titleEnd == ' '):
				title[i] = title[i][:-1]
				titleEnd = title[i][-1]
			
			strF1 += "⭕ *"+title[i]+"*\n\n"
			strAbhivyakti += "⭕ *"+title[i]+"*\n\n"

			strF1 += "✒️ "+author[i]+"\n\n_"+excerpt[i]+"_\n\n*Read full article:*\n"
			strAbhivyakti += "✒️ "+author[i]+"\n\n_"+excerpt[i]+"_\n\n*Read full article:*\n"

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