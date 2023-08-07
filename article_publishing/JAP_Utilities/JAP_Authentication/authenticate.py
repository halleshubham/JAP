import json
import os
from creds_parser import get_creds

def get_creds():
    creds = get_creds()
    if "resource_owner_key" not in creds.keys():
        print("Access Token not found!! Please run the authorize.py first!")
        return False
    else:
        return creds
