import http.client

conn = http.client.HTTPConnection("janataweekly.org")

username=input("Username?")
password=input("Pass?")

payload = "{\n\t\"username\":\""+username+"\",\n\t\"password\":\""+password+"\"\n}"

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

conn.request("POST", "/wp-json/jwt-auth/v1/token", payload, headers)

res = conn.getresponse()
data = res.read()

tokendata = json.loads(data.decode("utf-8"))

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'Authorization': "Bearer "+tokendata["token"]
    }

#post = {"title":"new temp post"}
payload = json.dumps(post)

#conn.request("POST", "/wp-json/wp/v2/posts", payload, headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))