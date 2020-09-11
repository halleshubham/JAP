import requests
import http.client
import json
import datetime
import re
import facebook
from datetime import timezone
import sys
import time

def getArticle(access_token,pageID):
	graph = facebook.GraphAPI(access_token=access_token)
	#b=319140888763658
	a= graph.get_object(
		id=(str(pageID)+'/scheduled_posts'),
		fields=("id")) 
	return a

def getArticlesDeleted(toBeDeleted,pageID,access_token):
	a = getArticle(access_token,pageID)
	q=0
	sum=len(a["data"])
	while (q<sum):
		graph = facebook.GraphAPI(access_token=access_token)
		b = a["data"][q]["id"]
		data = a["data"][q]
		attachmentName = "attachments"

		c = graph.delete_object(id =b)
		print (c)
		q=q+1
	print("Completed")

creds_path="jap_conf.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds=json.load(f)

dellete = getArticlesDeleted(creds["YesDeletePosts"],creds["graph_Page_ID"],creds["graph_API_Key"])