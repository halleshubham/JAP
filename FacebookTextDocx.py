import http.client
import json
import datetime
import re
import unicodedata
import docx

document = docx.Document("E:/Lok/Janata/Summary_Janata_July 26.docx")

author=[]
excerpt=[]
title=[]

authorNumber=4
titleNumber=2
excerptNumber=6

for para in document.paragraphs:
    if (para.text != '') and (para.text != ' '):
        if (len(author)== len(excerpt)==len(title)): 
            title1=para.text
            title1=title1.split('. ',1)
            title.append(unicodedata.normalize("NFKD",title1[1]))
            continue
        if (len(excerpt)==len(author)) and (len(excerpt)!=len(title)):
            author.append(unicodedata.normalize("NFKD",para.text))
            continue
        if (len(author)==len(title)) and (len(excerpt)!=len(author)):
            excerpt.append(unicodedata.normalize("NFKD",para.text))
            continue

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