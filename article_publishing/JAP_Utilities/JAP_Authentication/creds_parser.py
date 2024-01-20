import json
import os

def get_creds():
    creds_path = './article_publishing/Configs/jap_config.json'
    if os.path.exists(creds_path):
        with open(creds_path) as creds_file:
            creds = json.load(creds_file)
            """if "resource_owner_key" not in creds.keys():
                 print("Access Token not found!! Please run the authorize.py first!")
                 return False
            else:"""
            return creds
    else:
        print('Error : jap_config.json missing!')