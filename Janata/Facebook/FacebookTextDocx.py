import http.client
import json
import datetime
import re
import unicodedata
import docx

def get_Facebook_Txt_For_Kedar(summary):
	author= summary[0]['authors']
	excerpt=summary[0]['excerpts']
	title=summary[0]['titles']

	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache"
		}

	conn.request("GET", "/wp-json/wp/v2/posts?per_page=30")
	res = conn.getresponse()
	data = json.loads(res.read())

	refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')
	l=len(author)
	j=0
	i=l
	strF1=''
	while j<l:
		if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
			strF1 += str(j+1)+"\n"+title[j]+"\n\n"
			strF1 += author[j]+"\n\n"+excerpt[j]+"\n\nRead full article:\n"
			strF1 += data[i]["link"]+"\n\n"
			j=j+1
		i=i-1
	print (strF1)

	f3 = open("Facebook_Docx.txt","w",encoding="UTF-8")
	f3.write(strF1)
	f3.close()