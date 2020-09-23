import requests
import http.client
import json
import datetime
import re
import facebook
from datetime import timezone
import sys
import time

def getArticle():
	graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBALizI7Ou26PxEbhnq80u2K1d1XSMPT3AOQ1BKF6UW47qQ2diQkklI2oCj5mPTiSdk2p3sMf3ZBTqGt7IkWPrh3pk8CTUaU0ZBN7qZBiHZClZA8z4IIvjMAGRntMcdJjHL19mtNx8ZB0I3PfGXWNW48hZB6BK28o3eDEZA3YuASOzEwbG01HhVNx6RaiA1ZA7OGAZDZD")
	b=319140888763658
	
	a= graph.get_object(
		id='319140888763658/posts',
		fields=("id","attachments{media}")) 
	return a

a = getArticle()
q=0

sum=len(a["data"])
while (q<sum):
	graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBALizI7Ou26PxEbhnq80u2K1d1XSMPT3AOQ1BKF6UW47qQ2diQkklI2oCj5mPTiSdk2p3sMf3ZBTqGt7IkWPrh3pk8CTUaU0ZBN7qZBiHZClZA8z4IIvjMAGRntMcdJjHL19mtNx8ZB0I3PfGXWNW48hZB6BK28o3eDEZA3YuASOzEwbG01HhVNx6RaiA1ZA7OGAZDZD")
	b = a["data"][q]["id"]
	data = a["data"][q]
	attachmentName = "attachments"
	if attachmentName in data:
		attachment = a["data"][q]["attachments"]
		media = a["data"][q]["attachments"]["data"][0]["media"]
		print("Key exist for",q)
	else:
		print("Key doesn't exist for",q)
	if (bool(attachment) == False):
		i=1
	#c = graph.delete_object(id =b)
	q=q+1
print("Completed")
