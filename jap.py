from JAP_Authentication.authenticate import get_creds
from DocParser.parse_doc import get_summary_data
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import json
import os
from pprint import pprint
import unidecode



def get_authors_list(summary_data):
    authors_list = []
    for article in summary_data:
        authors_list.append(article['article_author'])
    return authors_list



def get_author_by_slug(author,creds):
    username_pre=''.join(e for e in author if e.isalnum()) # for removing all the special charathers 
    username = unidecode.unidecode(username_pre)[:49]
    protected_url='https://janataweekly.org/wp-json/wp/v2/users?slug='+username

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



def get_author_by_email(author,creds):
    username_pre=''.join(e for e in author if e.isalnum()) # for removing all the special charathers 
    username = unidecode.unidecode(username_pre)[:49]
    protected_url='https://janataweekly.org/wp-json/wp/v2/users?search='+username+'@test.com'
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
    username_pre=''.join(e for e in author if e.isalnum()) # for removing all the special charathers 
    username = unidecode.unidecode(username_pre)[:49]

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
    if r.status_code == 201:
        return r.json()['id']
    else:
        error = r.json()
        if error['code'] == 'existing_user_email':
            existing_author_id = get_author_by_email(author,creds)
            if existing_author_id:
                update_status = update_author(author,existing_author_id,creds)
                if update_status:
                    return True
                else:    
                    return False
        else:
            pprint(error)
            return False



def update_author(author,existing_author_id,creds):
    username_pre=''.join(e for e in author if e.isalnum()) # for removing all the special charathers 
    username = unidecode.unidecode(username_pre)[:49]
    protected_url='https://janataweekly.org/wp-json/wp/v2/users/'+str(existing_author_id)
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    data={
            'first_name' : author ,
            'slug' : username

            }
    oauth = OAuth1Session(    
                            creds['client_key'],
                            client_secret=creds['client_secret'],
                            resource_owner_key=creds['resource_owner_key'],
                            resource_owner_secret=creds['resource_owner_secret']
                        )
    r = oauth.post(protected_url,headers=headers,data=data)
    if r.status_code == 200:
        return r.json()['id']
    else:
        print(r.json())
        return False



def add_authors(authors_list,creds):
    author_ids=[]
    author_added_count=0
    for author in authors_list:
        author_id=get_author_by_slug(author,creds)
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



def upload_images(folder_path,creds,author_ids_list_length):
    if len(os.listdir(folder_path))==author_ids_list_length:
        protected_url='https://janataweekly.org/wp-json/wp/v2/media/'
        headers = { 
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                    }
        image_ids={}
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
                print(r.content)
                return {'status':False,'image_ids':image_ids,'message':'Error uploading image'}
            image_number=image_file.split('.')[0]
            image_ids[image_number]=r.json()['id']
            print('Image "' + image_file +'" uploaded successfully')    
        return {'status':True,'image_ids':image_ids}
    else:
        return {'status':False,'image_ids':{},'message':'Number of images and articles does not match!'}

def delete_images(id_list,creds):
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    oauth = OAuth1Session(    
                                creds['client_key'],
                                client_secret=creds['client_secret'],
                                resource_owner_key=creds['resource_owner_key'],
                                resource_owner_secret=creds['resource_owner_secret']
                            )
    for id in id_list:
        protected_url='https://janataweekly.org/wp-json/wp/v2/media/'+str(id)+'?force=true'
        r = oauth.delete(protected_url,headers=headers)
        if r.status_code!=200:
            print(r.status_code)
            print(r.text)
        #print(r.josn())
    print("Deleted old images!")


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
        print(r.text)
        return False
    else:
        return True