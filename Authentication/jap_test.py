from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json

with open("jap_config.json") as f:
    creds=json.load(f)

if "resource_owner_key" not in creds.keys():
    print("Access Token not found!! Please run the authorize.py first!")
else:
    protected_url='http://janataweekly.org/wp-json/wp/v2/users/me'

    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                }



    oauth = OAuth1Session(    
                            creds['client_key'],
                            client_secret=creds['client_secret'],
                            resource_owner_key=creds['resource_owner_key'],
                            resource_owner_secret=creds['resource_owner_secret']
                        )

    r = oauth.get(protected_url,headers=headers)

    print(r.content)