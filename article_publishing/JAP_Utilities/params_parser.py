import json

def get_params():
    with open('./article_publishing/Configs/issue_params.json') as params_file:
        return json.load(params_file)
    