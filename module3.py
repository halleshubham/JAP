import requests
import http.client
import json
import datetime
import re
import facebook
from datetime import timezone
import sys
import time

def getArticleAttachment(id1):
	graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBALizI7Ou26PxEbhnq80u2K1d1XSMPT3AOQ1BKF6UW47qQ2diQkklI2oCj5mPTiSdk2p3sMf3ZBTqGt7IkWPrh3pk8CTUaU0ZBN7qZBiHZClZA8z4IIvjMAGRntMcdJjHL19mtNx8ZB0I3PfGXWNW48hZB6BK28o3eDEZA3YuASOzEwbG01HhVNx6RaiA1ZA7OGAZDZD")
	a= graph.get_object(
		id=id1,
		fields=("message","attachments{media}"))
	return a

id='319140888763658_552832158727862'
a = getArticleAttachment(id)
q=0
attachmentName = "attachments"
graph = facebook.GraphAPI(access_token="EAAObhNZCDIcUBALizI7Ou26PxEbhnq80u2K1d1XSMPT3AOQ1BKF6UW47qQ2diQkklI2oCj5mPTiSdk2p3sMf3ZBTqGt7IkWPrh3pk8CTUaU0ZBN7qZBiHZClZA8z4IIvjMAGRntMcdJjHL19mtNx8ZB0I3PfGXWNW48hZB6BK28o3eDEZA3YuASOzEwbG01HhVNx6RaiA1ZA7OGAZDZD")

if attachmentName in a:
	attachment = a["data"][q]["attachments"]
	media = a["data"][q]["attachments"]["data"][0]["media"]
	print("Key exist for",q)
else:
	print("Key doesn't exist for",q)
	graph.put_object(parent_object=id,connection_name=id,
                  message='https://janataweekly.org/wp-content/uploads/2020/06/index-4.jpg!')

if (bool(attachment) == False):
	i=1
#c = graph.delete_object(id =b)
print("Completed")
