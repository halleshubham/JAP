from requests_oauthlib import OAuth1Session
from multiprocessing import Pool
import os
from pprint import pprint
import unidecode
from slugify import slugify
import requests
import re
import requests
from io import BytesIO
import base64
import re


def extract_base64_inline_images(html):
    base64_images = re.findall(r'<img[^>]+src="data:image/[^;]+;base64[^"]+"', html)
    return base64_images

# Commented out OAuth version
# def upload_inline_image_to_wordpress(image_data, image_filename, creds):
#     image_data = re.sub('^data:image/.+;base64,', '', image_data)
#     image_bytes = base64.b64decode(image_data)
#     protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/'
#     headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
#                 }
    
#     data = {
#         'file': (image_filename, BytesIO(image_bytes))
#     }
#     oauth = OAuth1Session(creds['client_key'],
#                                     client_secret=creds['client_secret'],
#                                     resource_owner_key=creds['resource_owner_key'],
#                                     resource_owner_secret=creds['resource_owner_secret'])
#     r = oauth.post(protected_url,headers=headers,files=data)
   
#     return r.json()

def upload_inline_image_to_wordpress(image_data, image_filename, creds):
    """Upload inline image using basic authentication"""
    import base64 as b64
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return False
    
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_bytes = base64.b64decode(image_data)
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/'
    
    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = b64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    files = {
        'file': (image_filename, BytesIO(image_bytes))
    }
    
    r = requests.post(protected_url, headers=headers, files=files)
    
    if r.status_code == 401:
        print("401 Unauthorized error uploading inline image")
        print("Please check your WordPress username and password")
        return False
    
    if r.status_code != 201:
        print(f"Error uploading inline image: {r.status_code} - {r.text}")
        return False
   
    return r.json()

def process_base64_inline_images(html, creds):
    base64_images = extract_base64_inline_images(html)
    for img_tag in base64_images:
        base64_data = re.search(r'src="(data:image/[^;]+;base64[^"]+)"', img_tag).group(1)
        # Generate a unique filename or use a static one if you prefer
        image_filename = 'uploaded_image.png'
        response = upload_inline_image_to_wordpress(base64_data, image_filename, creds)
        image_url = response['source_url']
        # Replace the base64 image in the HTML with the URL of the uploaded image
        html = html.replace(base64_data, image_url)
    return html

def get_authors_list(summary_data):
    authors_list = []
    for article in summary_data:
        authors_list.append(article['article_author'])
    return authors_list



# Commented out OAuth version due to 401 errors
# def get_author_by_slug(author,creds):
#     username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
#     username = unidecode.unidecode(username_pre)[:49]
#     protected_url = 'https://janataweekly.org/wp-json/wp/v2/users?slug=' + username

#     headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
#                 }
#     oauth = OAuth1Session(creds['client_key'],
#                             client_secret=creds['client_secret'],
#                             resource_owner_key=creds['resource_owner_key'], 
#                             resource_owner_secret=creds['resource_owner_secret'])
#     r = oauth.get(protected_url,headers=headers)
#     if len(r.json()) == 0:
#         return False
#     else :
#         author = r.json()[0]['id']
#         return author

def get_author_by_slug(author, creds):
    """Get author by slug using basic authentication"""
    import base64
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return False
    
    username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
    username = unidecode.unidecode(username_pre)[:49]
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/users?slug=' + username

    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    r = requests.get(protected_url, headers=headers)
    
    if r.status_code == 401:
        print(f"401 Unauthorized error in get_author_by_slug for author: {author}")
        print("Please check your WordPress username and password")
        return False
    
    if r.status_code != 200:
        print(f"HTTP Error {r.status_code} in get_author_by_slug for author: {author}")
        print(f"Response: {r.text}")
        return False
        
    if len(r.json()) == 0:
        return False
    else:
        author_id = r.json()[0]['id']
        return author_id



# Commented out OAuth version due to 401 errors
# def get_author_by_email(author,creds):
#     username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
#     username = unidecode.unidecode(username_pre)[:49]
#     protected_url = 'https://janataweekly.org/wp-json/wp/v2/users?search=' + username + '@test.com'
#     headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
#                 }
#     oauth = OAuth1Session(creds['client_key'],
#                             client_secret=creds['client_secret'],
#                             resource_owner_key=creds['resource_owner_key'], 
#                             resource_owner_secret=creds['resource_owner_secret'])

      
#     r = oauth.get(protected_url,headers=headers)
#     if len(r.json()) == 0:
#         return False
#     else :
#         author = r.json()[0]['id']
#         return author

def get_author_by_email(author, creds):
    """Get author by email using basic authentication"""
    import base64
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return False
    
    username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
    username = unidecode.unidecode(username_pre)[:49]
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/users?search=' + username + '@test.com'
    
    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    r = requests.get(protected_url, headers=headers)
    
    if r.status_code == 401:
        print(f"401 Unauthorized error in get_author_by_email for author: {author}")
        print("Please check your WordPress username and password")
        return False
    
    if r.status_code != 200:
        print(f"HTTP Error {r.status_code} in get_author_by_email for author: {author}")
        print(f"Response: {r.text}")
        return False
        
    if len(r.json()) == 0:
        return False
    else:
        author_id = r.json()[0]['id']
        return author_id



def create_author(args):
    (author,creds) = args

    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return False

    author_id = get_author_by_slug(author,creds)
    if not author_id:
        import base64
        
        protected_url = 'https://janataweekly.org/wp-json/wp/v2/users'
        
        # Create basic auth header
        credentials = f"{creds['wp_username']}:{creds['wp_password']}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
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
        
        r = requests.post(protected_url, headers=headers, json=data)
        
        if r.status_code == 201:
            print('Author ' + author + ' added.')
            return r.json()['id']
            
        else:
            if r.status_code == 401:
                print(f"401 Unauthorized error creating author: {author}")
                print("Please check your WordPress username and password")
                return False
                
            try:
                error = r.json()
                if error['code'] == 'existing_user_email' or error['code'] == 'existing_user_login':
                    existing_author_id = get_author_by_email(author,creds)
                    if existing_author_id:
                        update_status = update_author(author,existing_author_id,creds)
                        if update_status:
                            return update_status
                        else: 
                            print('Author ' + author + ' could not be added.')
                            return False
                else:
                    pprint(error)
                    print('Author ' + author + ' could not be added.')
                    return False
            except:
                print(f"Error creating author {author}: {r.status_code} - {r.text}")
                return False
    else:
        print('Author ' + author + ' already present.')
        return author_id
        


def update_author(author,existing_author_id,creds):
    """Update author using basic authentication"""
    import base64
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return False
    
    username_pre = ''.join(e for e in author if e.isalnum()) # for removing all the special charathers
    username = unidecode.unidecode(username_pre)[:49]
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/users/' + str(existing_author_id)
    
    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }
    
    data = {
            'first_name' : author ,
            'slug' : username
            }
    
    r = requests.post(protected_url, headers=headers, json=data)
    
    if r.status_code == 200:
        return r.json()['id']
    else:
        if r.status_code == 401:
            print(f"401 Unauthorized error updating author: {author}")
            print("Please check your WordPress username and password")
        else:
            print(f"Error updating author {author}: {r.status_code}")
            try:
                print(r.json())
            except:
                print(r.text)
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

# Commented out OAuth version
# def upload_image(args):
#     (image_file, folder_path, creds) = args

#     protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/'
#     headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
#                 }
#     data = {
#                'file': open(folder_path + image_file,'rb')
#            }
#     oauth = OAuth1Session(creds['client_key'],
#                                     client_secret=creds['client_secret'],
#                                     resource_owner_key=creds['resource_owner_key'],
#                                     resource_owner_secret=creds['resource_owner_secret'])
#     r = oauth.post(protected_url,headers=headers,files=data)
#     if r.status_code != 201:
#         print('Image "' + image_file + '" could not be uploaded')
#         print(r.content)
#         return {'status': False, 'message' : 'Error uploading image'}

#     image_number = image_file.split('.')[0]
#     image_id= r.json()['id']
#     print('Image "' + image_file + '" uploaded successfully') 
#     return {'status': True, 'image_number': image_number, 'image_id': image_id  }


# def convert_image_to_jpg(image_path):
#     from PIL import Image
#     img = Image.open(image_path)
#     # Convert to RGB for JPEG
#     if img.mode != "RGB":
#         img = img.convert("RGB")
#     jpg_image_path = os.path.splitext(image_path)[0] + '.jpg'
#     img.save(jpg_image_path, 'JPEG', quality=95)
#     os.remove(image_path)
#     return jpg_image_path

def convert_and_optimize_image(image_path, max_size=819200):
    from PIL import Image
    import io
    # Always convert PNG to JPEG for best size reduction
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Prepare output JPEG path
    jpeg_path = os.path.splitext(image_path)[0] + ".jpg"
    quality = 95
    min_quality = 20
    resize_factor = 0.9
    min_size = (200, 200)  # Don't shrink below this
    # Start with original size
    width, height = img.size
    while True:
        # Save to buffer to check size
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        size = buf.tell()
        if size <= max_size:
            # Write to disk
            with open(jpeg_path, "wb") as f:
                f.write(buf.getvalue())
            # Remove original PNG
            try:
                os.remove(image_path)
            except Exception:
                pass
            return jpeg_path
        # Reduce quality if possible
        if quality > min_quality:
            quality -= 10
            continue
        # If quality is low, try resizing
        if width > min_size[0] and height > min_size[1]:
            width = int(width * resize_factor)
            height = int(height * resize_factor)
            img = img.resize((width, height), Image.LANCZOS)
            # Reset quality for new size
            quality = 95
            continue
        # If can't reduce further, save as is and break
        with open(jpeg_path, "wb") as f:
            f.write(buf.getvalue())
        try:
            os.remove(image_path)
        except Exception:
            pass
        return jpeg_path


def upload_image(args):
    """Upload image using basic authentication"""
    import base64
    
    (image_file, folder_path, creds) = args

    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return {'status': False, 'message': 'Basic auth credentials missing'}

    protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/'
    
    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}'
    }

    optimized_image_path = convert_and_optimize_image(folder_path + image_file)
    
    files = {
        'file': open(optimized_image_path, 'rb')
    }
    
    r = requests.post(protected_url, headers=headers, files=files)
    
    if r.status_code == 401:
        print('401 Unauthorized error uploading image "' + image_file + '"')
        print("Please check your WordPress username and password")
        return {'status': False, 'message': 'Unauthorized'}
    
    if r.status_code != 201:
        print('Image "' + image_file + '" could not be uploaded')
        print(f"Status: {r.status_code}, Response: {r.text}")
        return {'status': False, 'message': 'Error uploading image'}

    image_number = image_file.split('.')[0]
    image_id = r.json()['id']
    print('Image "' + image_file + '" uploaded successfully') 
    return {'status': True, 'image_number': image_number, 'image_id': image_id}


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

# Commented out OAuth version
# def delete_image(args):
#     (image_id,creds) = args
#     headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
#                 }
#     oauth = OAuth1Session(creds['client_key'],
#                                 client_secret=creds['client_secret'],
#                                 resource_owner_key=creds['resource_owner_key'],
#                                 resource_owner_secret=creds['resource_owner_secret'])
#     protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/' + str(image_id) + '?force=true'
#     r = oauth.delete(protected_url,headers=headers)
#     if r.status_code != 200:
#         print(r.status_code)
#         print(r.text)

def delete_image(args):
    """Delete image using basic authentication"""
    import base64
    
    (image_id, creds) = args
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return
    
    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/media/' + str(image_id) + '?force=true'
    r = requests.delete(protected_url, headers=headers)
    
    if r.status_code == 401:
        print("401 Unauthorized error deleting image")
        print("Please check your WordPress username and password")
    elif r.status_code != 200:
        print(f"Error deleting image {image_id}: {r.status_code}")
        print(r.text)

def delete_images(id_list,creds):
    total_delete_payload = []
    for image_id in id_list:
        total_delete_payload.append((image_id,creds))
    with Pool() as pool:
        results = pool.map(delete_image, total_delete_payload)
    print("Deleted the images uploaded in this session!")


# Commented out OAuth version
# def create_post(args):
#     (data,creds) = args
#     try:
#         protected_url = 'https://janataweekly.org/wp-json/wp/v2/posts/'
#         headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 
#                 }

#         oauth = OAuth1Session(creds['client_key'],
#                                     client_secret=creds['client_secret'],
#                                     resource_owner_key=creds['resource_owner_key'],
#                                     resource_owner_secret=creds['resource_owner_secret'])

#         r = oauth.post(protected_url,headers=headers,data=data)
#         if r.status_code != 201:
#             print(r.text)
#             print("Post could not be created for article: ", data['title'])
#             return {'status': False, 'article_title': data['title']}
#         else:
#             print("Post created for article: ", data['title'])
#             article_id = r.json()['id']
#             return {'status': True, 'article_title': data['title'], 'article_id':article_id}
#     except Exception as e:
#         print(e)
#         print("Could not create the draft for the article ", data['title'])
#         return {'status': False, 'article_title': data['title']}

def create_post(args):
    """Create post using basic authentication"""
    import base64
    
    (data, creds) = args
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return {'status': False, 'article_title': data['title']}
    
    try:
        protected_url = 'https://janataweekly.org/wp-json/wp/v2/posts/'
        
        # Create basic auth header
        credentials = f"{creds['wp_username']}:{creds['wp_password']}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }

        r = requests.post(protected_url, headers=headers, json=data)
        
        if r.status_code == 401:
            print("401 Unauthorized error creating post for article:", data['title'])
            print("Please check your WordPress username and password")
            return {'status': False, 'article_title': data['title']}
        
        if r.status_code != 201:
            print(f"Error {r.status_code} creating post for article: {data['title']}")
            print(r.text)
            return {'status': False, 'article_title': data['title']}
        else:
            print("Post created for article: ", data['title'])
            article_id = r.json()['id']
            return {'status': True, 'article_title': data['title'], 'article_id': article_id}
    except Exception as e:
        print(e)
        print("Could not create the draft for the article ", data['title'])
        return {'status': False, 'article_title': data['title']}

# Commented out OAuth version
# def delete_post(args):
#     (article_id,creds) = args
#     headers = { 
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                     
#                 }
#     oauth = OAuth1Session(creds['client_key'],
#                                 client_secret=creds['client_secret'],
#                                 resource_owner_key=creds['resource_owner_key'],
#                                 resource_owner_secret=creds['resource_owner_secret'])
#     protected_url = 'https://janataweekly.org/wp-json/wp/v2/posts/' + str(article_id) + '?force=true'
#     r = oauth.delete(protected_url,headers=headers)
#     if r.status_code != 200:
#         print(r.status_code)
#         print(r.text)

def delete_post(args):
    """Delete post using basic authentication"""
    import base64
    
    (article_id, creds) = args
    
    # Check if basic auth credentials are available
    if 'wp_username' not in creds or 'wp_password' not in creds:
        print("Basic auth credentials (wp_username, wp_password) not found in config")
        return
    
    # Create basic auth header
    credentials = f"{creds['wp_username']}:{creds['wp_password']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    protected_url = 'https://janataweekly.org/wp-json/wp/v2/posts/' + str(article_id) + '?force=true'
    r = requests.delete(protected_url, headers=headers)
    
    if r.status_code == 401:
        print("401 Unauthorized error deleting post")
        print("Please check your WordPress username and password")
    elif r.status_code != 200:
        print(f"Error deleting post {article_id}: {r.status_code}")
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
        print(article_url)
        print("Could not get the url for the article: " +article_title)
        return False
    else:
        return (article_title, article_url)

def get_article_urls(article_titles):
    #results={}
    #for title in article_titles:
        #results = get_article_url(title)
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