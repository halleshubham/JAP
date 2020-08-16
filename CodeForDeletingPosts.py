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
	graph = facebook.GraphAPI(access_token="EAAYY9ZBJvM0QBAO1oUJ9IljG5TAXuOcJBXakznXhMYuMZBzpGCVYv8wbw3PFxSZBgb79jj79pzbNgP5kRedEHYqkPXTZANsB7Vd9WiNM4DxS9uQZCt8DCYpx0Pg6WsaS3OuIs078b6aNZAkaEz45ZCZCtpQSfm8XRmBfb0XMKZCIIkUt7AvHu84GD1ysi6MDCl6FWTaIBMQ4h13vB4ZB5qPOTr")
	#b=319140888763658
	a= graph.get_object(
		id='108144264067982/scheduled_posts',
		fields=("id")) 
	return a

a = getArticle()
q=0
sum=len(a["data"])
while (q<sum):
	graph = facebook.GraphAPI(access_token="EAAYY9ZBJvM0QBAO1oUJ9IljG5TAXuOcJBXakznXhMYuMZBzpGCVYv8wbw3PFxSZBgb79jj79pzbNgP5kRedEHYqkPXTZANsB7Vd9WiNM4DxS9uQZCt8DCYpx0Pg6WsaS3OuIs078b6aNZAkaEz45ZCZCtpQSfm8XRmBfb0XMKZCIIkUt7AvHu84GD1ysi6MDCl6FWTaIBMQ4h13vB4ZB5qPOTr")
	b = a["data"][q]["id"]
	data = a["data"][q]
	attachmentName = "attachments"


	c = graph.delete_object(id =b)
	print (c)
	q=q+1
print("Completed")
