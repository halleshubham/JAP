import json
import os

def get_creds():
    creds_path = './article_publishing/Configs/jap_config.json'
    if os.path.exists(creds_path):
        with open(creds_path) as creds_file:
            return json.load(creds_file)
    else:
        print('Error : jap_config.json missing!')