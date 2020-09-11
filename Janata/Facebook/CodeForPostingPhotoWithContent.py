import requests
import http.client
import json
import datetime
import re
import facebook
from datetime import timezone
import sys
import time

graph = facebook.GraphAPI(access_token="EAAD9FSfHdf4BAPUEPDno8ndvYtM6LzuHdYPFZCZC1QhqUaqLSYMS1qZA2o4XoVPHkwxsJrUlLZB6hUr8RGbXZB2hSh8AhZAR6SWIPVU0P5CjZCZBfBZBTK38bvZBi3kM7RbimZAtPNcUj3ndCxdZCLzIHrxXmkoJ5TzoKWxxMmmxPZCu6VksbrA5AZBQNZCvoiTK3oGrN2xN04VZBT7QXQZDZD")

elevenAM= datetime.datetime(2020, 7, 3,5,40)
elevenAM = elevenAM.replace(tzinfo=timezone.utc).timestamp()

#Below code is for posting photo
b=108144264067982
a= graph.put_object(
	parent_object=str(b),
	connection_name="photos",
	published="false",
	url = 'https://janataweekly.org/wp-content/uploads/2020/06/21-Tim-.jpg',
	message='Uday Rocks',
	scheduled_publish_time=int(elevenAM))
	#full_picture=murl)
print (a)

b=108144264067982
id='108144264067982_177325060483235'
data = {
  'message': 'ROckstsar'
}
headers = {
    'access_token': 'EAAD9FSfHdf4BAPUEPDno8ndvYtM6LzuHdYPFZCZC1QhqUaqLSYMS1qZA2o4XoVPHkwxsJrUlLZB6hUr8RGbXZB2hSh8AhZAR6SWIPVU0P5CjZCZBfBZBTK38bvZBi3kM7RbimZAtPNcUj3ndCxdZCLzIHrxXmkoJ5TzoKWxxMmmxPZCu6VksbrA5AZBQNZCvoiTK3oGrN2xN04VZBT7QXQZDZD',
}

response = requests.post('https://graph.facebook.com/v7.0/108144264067982_177325060483235/', headers=headers,data=data)

a= graph.request(
	#parent_object=id,
	#published="false",
	parent_object='108144264067982_177325060483235',
	message='Uday Rocks')
	#scheduled_publish_time=tim,
	#is_hidden="false",
	#full_picture=murl)
print (a)