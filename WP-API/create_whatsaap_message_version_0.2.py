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


conn = http.client.HTTPConnection("janataweekly.org")

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

conn.request("GET", "/wp-json/wp/v2/posts?per_page=20")
res = conn.getresponse()
data = json.loads(res.read())

refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')

strF = '📮 *Janata Weekly*\n'
strF += '*Issue: '+ refDateObj.strftime('%d %B, %Y')+'*\n\n'
strF +='👍 https://facebook.com/JanataWeekly\n\n'
strF +='*Articles for this week*\n'
for i in range(0,20):
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		strF += ""+ str(i) +". "+data[i]["title"]["rendered"]+"\n"
		authorName = getAuthorName(data[i]["author"])
		print(authorName)
		strF += "By _"+authorName+"_\n"
		# strF += "By _AuthorName_\n"
		strF += data[i]["link"]+"\n-----------------------------------------------------------\n"

strF += "\n➖➖➖➖➖➖➖➖➖➖➖\n📋 *About Janata Weekly :*\nJanata Weekly is an independent socialist journal. It has raised its challenging voice of principled dissent against all conduct and practice that is detrimental to the cherished values of nationalism, democracy, secularism and socialism, while upholding the integrity and the ethical norms of healthy journalism. It has the enviable reputation of being the oldest continuously published socialist journal in India."
strF += "\n📢Oldest socialist weekly of India, is now also on facebook!\n"
strF += "📋 *Subscribe to Janata Weekly Hard Copy*\n\nAnnual: Rs. 260 /-\nThree Years : Rs. 750 /-\n\n📲 Guddi: 07738082170\n➖➖➖➖➖➖➖➖➖➖➖\n"
strF += "📬 To recieve Janata directly to your mailbox\nFill this form: http://tiny.cc/JoinJanataWeekly\n\n📬 Join for WhatsApp version \n"
strF += "🔴 Group 1: https://chat.whatsapp.com/GFy7sR6uV9bD9gt5dlhE7D\n\n🔴 Group 2: https://chat.whatsapp.com/Gvp7JM00VvZKMeh6ld302v"

print(strF)
f = open("whatsappMessage.txt","w",encoding="UTF-8")
f.write(strF)
f.close()
