import http.client
import json
import datetime
import re
import unicodedata
import docx
import json

def LokayatEnglishWhatsapp(summary):
	author= summary[0]['authors']
	excerpt=summary[0]['excerpts']
	title=summary[0]['titles']

	conn = http.client.HTTPSConnection("janataweekly.org")

	l=len(author)

	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache"
		}

	conn.request("GET", "/wp-json/wp/v2/posts?per_page=36")
	res = conn.getresponse()
	data = json.loads(res.read())

	refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')
	l=len(author)

	imp = "-----------------------------------------------------------\n 📱 _Join Lokayat's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/DxY7U42lGBeHyLJwUYCtn4\n\n"
	imp += "📱 _लोकायतचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/DQtYRIIuydR2fMTjTHVcOT\n\n"
	imp += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"
	j=0
	i=l
	strF1=""

	while j<l:
		if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:

			strF1 += "⭕ *"+title[j]+"*\n\n"
			strF1 += "✒️ "+author[j]+"\n\n_"+excerpt[j]+"_\n\n*Read full article:*\n"
			strF1 += data[i]["link"]+"\n\n"+imp
			j=j+1
		i=i-1
	print (strF1)

	f3 = open("EnglishWhatsappMessagesUsingDocx.txt","w",encoding="UTF-8")
	f3.write(strF1)
	f3.close()

