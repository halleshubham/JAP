from JAP_Authentication.authenticate import get_creds
from DocParser.parse_doc import get_summary_data
from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json
import os
from pprint import pprint



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
        author = r.json()[0]['id']
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
        return r.json()['id']



def add_authors(authors_list,creds):
    author_ids=[]
    author_added_count=0
    for author in authors_list:
        author_id=get_author(author,creds)
        if not author_id:
            author_id=create_author(author,creds)
            if author_id:
                print('Author '+author+' created successfuly.')
                author_added_count = author_added_count + 1
                author_ids.append(author_id)
            else :
                print('Author '+author+' could not be added.')
                return False
        else:
            author_ids.append(author_id)
            print('Author '+author+' already present.')
    print('Total authors created : ' + str(author_added_count))
    return author_ids



def upload_images(folder_path,creds):
    protected_url='https://janataweekly.org/wp-json/wp/v2/media/'
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                }
    image_ids=[]
    for image_file in os.listdir(folder_path):
        data ={
            'file': open(folder_path+image_file,'rb')
        }
 
        oauth = OAuth1Session(    
                                creds['client_key'],
                                client_secret=creds['client_secret'],
                                resource_owner_key=creds['resource_owner_key'],
                                resource_owner_secret=creds['resource_owner_secret']
                            )
        r = oauth.post(protected_url,headers=headers,files=data)
        if r.status_code!=201:
            print('Image "' + image_file +'" could not be uploaded')
            return False
        image_ids.append(r.json()['id'])
        print('Image "' + image_file +'" uploaded successfully')    
    return image_ids


def create_post(data,creds):
    protected_url='https://janataweekly.org/wp-json/wp/v2/posts/'
    headers = { 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
            }

    oauth = OAuth1Session(    
                                creds['client_key'],
                                client_secret=creds['client_secret'],
                                resource_owner_key=creds['resource_owner_key'],
                                resource_owner_secret=creds['resource_owner_secret']
                            )

    r = oauth.post(protected_url,headers=headers,data=data)
    if r.status_code!=201:
        return False
    else:
        return True


    
    
