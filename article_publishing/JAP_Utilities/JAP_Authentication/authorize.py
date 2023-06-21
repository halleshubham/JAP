from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json
import os

creds_path = "./article_publishing/JAP_Authentication/jap_config.json"
if os.path.exists(creds_path):
    with open(creds_path)  as f:
        creds=json.load(f)

urls={
        "request_token_url" : "https://janataweekly.org/oauth1/request",
        "base_authorization_url" : "https://janataweekly.org/oauth1/authorize",
        "access_token_url" : "https://janataweekly.org/oauth1/access",
        "call_back_url" : "https://janataweekly.org/"
     }


headers = { 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
            }

oauth = OAuth1Session(creds['client_key'], client_secret=creds['client_secret'],callback_uri=urls['call_back_url'])
fetch_response = oauth.fetch_request_token(urls['request_token_url'],headers=headers)

resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

authorization_url = oauth.authorization_url(urls['base_authorization_url'])
print ('Please go here and authorize,', authorization_url)
redirect_response = input('Paste the full redirect URL here: ')
oauth_response = oauth.parse_authorization_response(redirect_response)
verifier = oauth_response.get('oauth_verifier')

oauth = OAuth1Session(creds['client_key'],
                          client_secret=creds['client_secret'],
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)

oauth_tokens = oauth.fetch_access_token(urls['access_token_url'],headers=headers)
resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

token={
           "client_key": creds['client_key'],
           "client_secret":creds['client_secret'],
           "resource_owner_key" : resource_owner_key,
           "resource_owner_secret":resource_owner_secret  
       }

with open("./article_publishing/Configs/jap_config.json",'w') as f:
    json.dump(token,f)

print("Access token saved!")

