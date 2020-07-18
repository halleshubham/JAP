from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json

def get_creds():
    with open("JAP/JAP_Authentication/jap_config.json") as f:
        creds=json.load(f)

    if "resource_owner_key" not in creds.keys():
        print("Access Token not found!! Please run the authorize.py first!")
        return False
    else:
        return creds