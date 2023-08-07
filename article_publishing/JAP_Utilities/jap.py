from requests_oauthlib import OAuth1Session
from multiprocessing import Pool
import os
from pprint import pprint
import unidecode
from slugify import slugify
import requests


def get_authors_list(summary_data):
    authors_list = []
    for article in summary_data:
        authors_list.append(article['article_author'])
    return authors_list



def get_author_by_slug(author,creds):
    username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
    username = unidecode.unidecode(username_pre)[:49]
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/users?slug=' + username

    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                }
    oauth = OAuth1Session(creds['client_key'],
                            client_secret=creds['client_secret'],
                            resource_owner_key=creds['resource_owner_key'], 
                            resource_owner_secret=creds['resource_owner_secret'])
    r = oauth.get(protected_url,headers=headers)
    if len(r.json()) == 0:
        return False
    else :
        author = r.json()[0]['id']
        return author



def get_author_by_email(author,creds):
    username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
    username = unidecode.unidecode(username_pre)[:49]
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/users?search=' + username + '@test.com'
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                }
    oauth = OAuth1Session(creds['client_key'],
                            client_secret=creds['client_secret'],
                            resource_owner_key=creds['resource_owner_key'], 
                            resource_owner_secret=creds['resource_owner_secret'])

      
    r = oauth.get(protected_url,headers=headers)
    if len(r.json()) == 0:
        return False
    else :
        author = r.json()[0]['id']
        return author



def create_author(args):
    (author,creds) = args

    author_id = get_author_by_slug(author,creds)
    if not author_id:
        protected_url = 'https://janataweekly.org/wp-json/wp/v2/users'
        headers = { 
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                    }
        username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
        username = unidecode.unidecode(username_pre)[:49]

        email = username + '@test.com'
        data = {
                'username':username,
                'email':email,
                'first_name':author,
                'roles':'author',
                'password':'testpass@1234'
                }
        oauth = OAuth1Session(creds['client_key'],
                                client_secret=creds['client_secret'],
                                resource_owner_key=creds['resource_owner_key'],
                                resource_owner_secret=creds['resource_owner_secret'])
        r = oauth.post(protected_url,headers=headers,data=data)
        if r.status_code == 201:
            print('Author ' + author + ' added.')
            return r.json()['id']
            
        else:
            error = r.json()
            if error['code'] == 'existing_user_email' or error['code'] == 'existing_user_login':
                existing_author_id = get_author_by_email(author,creds)
                if existing_author_id:
                    update_status = update_author(author,existing_author_id,creds)
                    if update_status:
                        return True
                    else: 
                        print('Author ' + author + ' could not be added.')
                        return False
            else:
                pprint(error)
                print('Author ' + author + ' could not be added.')
                return False
    else:
        print('Author ' + author + ' already present.')
        return author_id
        


def update_author(author,existing_author_id,creds):
    username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
    username = unidecode.unidecode(username_pre)[:49]
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/users/' + str(existing_author_id)
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    data = {
            'first_name' : author ,
            'slug' : username

            }
    oauth = OAuth1Session(creds['client_key'],
                            client_secret=creds['client_secret'],
                            resource_owner_key=creds['resource_owner_key'],
                            resource_owner_secret=creds['resource_owner_secret'])
    r = oauth.post(protected_url,headers=headers,data=data)
    if r.status_code == 200:
        return r.json()['id']
    else:
        print(r.json())
        return False


def add_authors(authors_list,creds):
    author_ids = []
    author_added_count = 0
    args = []
    for author in authors_list:
        args.append((author, creds))

    with Pool() as pool:
        results = pool.map(create_author, args)
    for result in results:
        if result:
            author_ids.append(result)
            author_added_count = author_added_count + 1
        else:
            return False
    return author_ids

def upload_image(args):
    (image_file, folder_path, creds) = args

    protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/'
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                }
    data = {
               'file': open(folder_path + image_file,'rb')
           }
    oauth = OAuth1Session(creds['client_key'],
                                    client_secret=creds['client_secret'],
                                    resource_owner_key=creds['resource_owner_key'],
                                    resource_owner_secret=creds['resource_owner_secret'])
    r = oauth.post(protected_url,headers=headers,files=data)
    if r.status_code != 201:
        print('Image "' + image_file + '" could not be uploaded')
        print(r.content)
        return {'status': False, 'message' : 'Error uploading image'}

    image_number = image_file.split('.')[0]
    image_id= r.json()['id']
    print('Image "' + image_file + '" uploaded successfully') 
    return {'status': True, 'image_number': image_number, 'image_id': image_id  }


def upload_images(folder_path,creds,author_ids_list_length):
    if len(os.listdir(folder_path)) == author_ids_list_length:       
        image_ids = {}
        args=[]
        for image_file in os.listdir(folder_path):
            args.append((image_file, folder_path, creds))
        
        with Pool() as pool:
            results = pool.map(upload_image, args)
            
        statuses = []
        for result in results:
            if result['status']:
                image_ids[result['image_number']] = result['image_id']
            statuses.append(result['status'])
        if not all(statuses):       
            return {'status':False,'image_ids':image_ids,'message':'Error uploading image'}
        else:
            return {'status':True,'image_ids':image_ids}
    else:
        return {'status':False,'image_ids':{},'message':'Number of images and articles does not match!'}

def delete_image(args):
    (image_id,creds) = args
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    oauth = OAuth1Session(creds['client_key'],
                                client_secret=creds['client_secret'],
                                resource_owner_key=creds['resource_owner_key'],
                                resource_owner_secret=creds['resource_owner_secret'])
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/' + str(image_id) + '?force=true'
    r = oauth.delete(protected_url,headers=headers)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def delete_images(id_list,creds):
    total_delete_payload = []
    for image_id in id_list:
        total_delete_payload.append((image_id,creds))
    with Pool() as pool:
        results = pool.map(delete_image, total_delete_payload)
    print("Deleted the images uploaded in this session!")


def create_post(args):
    (data,creds) = args
    try:
        protected_url = 'https://janataweekly.org/wp-json/wp/v2/posts/'
        headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
                }

        oauth = OAuth1Session(creds['client_key'],
                                    client_secret=creds['client_secret'],
                                    resource_owner_key=creds['resource_owner_key'],
                                    resource_owner_secret=creds['resource_owner_secret'])

        r = oauth.post(protected_url,headers=headers,data=data)
        if r.status_code != 201:
            print(r.text)
            print("Post could not be created for article: ", data['title'])
            return {'status': False, 'article_title': data['title']}
        else:
            print("Post created for article: ", data['title'])
            article_id = r.json()['id']
            return {'status': True, 'article_title': data['title'], 'article_id':article_id}
    except Exception as e:
        print(e)
        print("Could not create the draft for the article ", data['title'])
        return {'status': False, 'article_title': data['title']}

def delete_post(args):
    (article_id,creds) = args
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    oauth = OAuth1Session(creds['client_key'],
                                client_secret=creds['client_secret'],
                                resource_owner_key=creds['resource_owner_key'],
                                resource_owner_secret=creds['resource_owner_secret'])
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/posts/' + str(article_id) + '?force=true'
    r = oauth.delete(protected_url,headers=headers)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def delete_posts(id_list,creds):
    total_delete_payload = []
    for article_id in id_list:
        total_delete_payload.append((article_id,creds))
    with Pool() as pool:
        results = pool.map(delete_post, total_delete_payload)
    print("Deleted the draft posts created in this session!")

def get_article_url(article_title):
    article_url = "https://janataweekly.org/" + slugify(article_title, to_lower=True)

	#checking the link
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        print("Could not get the url for the article: " +article_title)
        return False
    else:
        return (article_title, article_url)

def get_article_urls(article_titles):
    with Pool() as pool:
        results = pool.map(get_article_url, article_titles)

    return results

def get_article_data(article_title):
    headers = { 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
                }
    url = 'https://janataweekly.org/wp-json/wp/v2/posts?slug=' + slugify(article_title, to_lower=True)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Could not get the image url for the article: "+ article_title)
        return False
    else:
        j = response.json()[0]["jetpack_featured_media_url"]
        return (article_title, response.json()[0])

def get_articles_data(article_titles):
    with Pool() as pool:
        results = pool.map(get_article_data, article_titles)
    
    return results