import json
import os

def get_params():
    params_path = './article_publishing/Configs/issue_params.json'
    if os.path.exists(params_path):
        with open(params_path) as params_file:
            return json.load(params_file)
    else:
        print('Error : issue_params.json missing!')