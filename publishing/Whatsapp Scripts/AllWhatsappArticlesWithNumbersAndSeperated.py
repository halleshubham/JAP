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

def getSymbols(i):
	symbols = '0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟'
	x=str(i)
	if(len(x)==1):
		return((symbols[3*(int(i))])+(symbols[3*(int(i))+2]))
	else:
		i=str(i)
		a=getSymbols(i[0])
		b=getSymbols(i[1])
		return(a+b)

conn = http.client.HTTPConnection("janataweekly.org")

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

conn.request("GET", "/wp-json/wp/v2/posts?per_page=36")
res = conn.getresponse()
data = json.loads(res.read())

refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')
ntrF = '📮 *Janata Weekly*\n'
ntrF += 'India\'s oldest socialist magzine!\n\n'
ntrF += 'Vol.75, No. '+ str(datetime.date.today().isocalendar()[1] - 4) +' | '+refDateObj.strftime('%d %B, %Y')+' Issue\n\n'
ntrF += 'Editor: Dr.G.G. Parikh \nAssociate Editor: Neeraj Jain \nManaging Editor: Guddi\n\n'
strF1 = ''
strF2 = ''
strF3 = ''
j=1
l=0

for i in range(29,-1,-1):
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		l=l+1

for i in range(l,l-11,-1):
	print(getAuthorName(data[i]["author"]))
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		print(getSymbols(j))
		strF1 += ""+ getSymbols(j)+" *"+data[i]["title"]["rendered"]+"*\n"
		authorName = getAuthorName(data[i]["author"]) 
		print(authorName)
		strF1 += "\n_By "+authorName+"_\n\n"
		# strF += "By _AuthorName_\n"
		strF1 += data[i]["link"] +"\n-----------------------------------------------------------\n\n" # + "\n IMAGE: " + \
		# data[i]["jetpack_featured_media_url"]
		j=j+1
print (strF1)

for i in range(l-11,l-27,-1):
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		print(getSymbols(j))
		strF2 += ""+ getSymbols(j)+" *"+data[i]["title"]["rendered"]+"*\n"
		authorName = getAuthorName(data[i]["author"]) 
		print(authorName)
		strF2 += "\n_By "+authorName+"_\n\n"
		# strF += "By _AuthorName_\n"
		strF2 += data[i]["link"] +"\n-----------------------------------------------------------\n\n" # + "\n IMAGE: " + \
		# data[i]["jetpack_featured_media_url"]
		j=j+1
print (strF2)

for i in range(l-27,l-36,-1):
	print(data[i]["author"])
	if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
		print(getSymbols(j))
		strF3 += ""+ getSymbols(j)+" *"+data[i]["title"]["rendered"]+"*\n"
		authorName = getAuthorName(data[i]["author"]) 
		print(authorName)
		strF3 += "\n_By "+authorName+"_\n\n"
		# strF += "By _AuthorName_\n"
		strF3 += data[i]["link"] +"\n-----------------------------------------------------------\n\n" # + "\n IMAGE: " + \
		# data[i]["jetpack_featured_media_url"]
		j=j+1

ntrF3 = "\n➖➖➖➖➖➖➖➖➖➖➖\n\n📋 *About Janata Weekly :*\nJanata Weekly is an *independent socialist journal*. It has raised its challenging voice of principled dissent against all conduct and practice that is detrimental to the cherished values of nationalism, democracy, secularism and socialism, while upholding the integrity and the ethical norms of healthy journalism. It has the enviable reputation of being the oldest continuously published socialist journal in India."
ntrF3 += "\n\n📢Oldest socialist weekly of India, is now also on facebook!\n"
ntrF3 +='👍 https://facebook.com/JanataWeekly \n\n'
ntrF3 += "📋 *Subscribe to Hard Copy*\n\nAnnual: Rs. 260 /-\nThree Years : Rs. 750 /-\n\n📲 Guddi: 07738082170\n➖➖➖➖➖➖➖➖➖➖➖\n\n"
ntrF3 += "📬 *To recieve Janata directly to your mailbox*\n\nFill this form: http://tiny.cc/JoinJanataWeekly\n\n📬 *Join for WhatsApp version* \n"
ntrF3 += "\n*🔴 Group 1*: https://chat.whatsapp.com/GFy7sR6uV9bD9gt5dlhE7D\n\n*🔴 Group 2*: https://chat.whatsapp.com/Gvp7JM00VvZKMeh6ld302v"

ntrF1= ntrF + strF1 + ntrF3
ntrF2= ntrF + strF2 + ntrF3
ntrF4= ntrF + strF3 + ntrF3

f1 = open("whatsappMessage1.txt","w",encoding="UTF-8")
f1.write(ntrF1)
f1.close()

f2 = open("whatsappMessage2.txt","w",encoding="UTF-8")
f2.write(ntrF2)
f2.close()

f3 = open("whatsappMessage3.txt","w",encoding="UTF-8")
f3.write(ntrF4)
f3.close()
