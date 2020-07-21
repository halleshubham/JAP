from JAP_Authentication.authenticate import get_creds
from DocParser.parse_doc import get_summary_data
from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json



def get_authors_list(summary_data):
    authors_list = []
    for article in summary_data:
        authors_list.append(article['article_author'])
    return authors_list



def get_author(author,creds):
    username=''.join(e for e in author if e.isalnum())
    protected_url='https://janataweekly.org/wp-json/wp/v2/users?search='+username
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
    if len(r.json()) == 0:
        return False
    else :
        author = r.json()[0]
        return author



def create_author(author,creds):
    protected_url='https://janataweekly.org/wp-json/wp/v2/users'
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    username=''.join(e for e in author if e.isalnum()) # for removing all the special charathers 
    email=username+'@test.com'
    data={
            'username':username,
            'email':email,
            'first_name':author,
            'roles':'author',
            'password':'testpass@1234'
            }
    oauth = OAuth1Session(    
                            creds['client_key'],
                            client_secret=creds['client_secret'],
                            resource_owner_key=creds['resource_owner_key'],
                            resource_owner_secret=creds['resource_owner_secret']
                        )
    r = oauth.post(protected_url,headers=headers,data=data)
    if r.status_code != 201:
        return False
    else:
        return True



def add_authors(authors_list):
    creds = get_creds()
    if creds:
        author_added_count=0
        for author in authors_list:
            retrieved_author=get_author(author,creds)
            if not retrieved_author:
                status=create_author(author,creds)
                if status:
                    print('Author '+author+' created successfuly.')
                    author_added_count = author_added_count + 1
                else :
                    print('Author '+author+' could not be added.')
            else:
                print('Author '+author+' already present.')
        print('Total authors created : ' + str(author_added_count))



    
    
