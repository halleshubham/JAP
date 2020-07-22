from JAP_Authentication.authenticate import get_creds
from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json
from pprint import pprint
import os
from jap import upload_images,get_summary_data,get_authors_list,add_authors,create_post
from datetime import datetime
import mammoth


creds=get_creds()

if creds:
    # getting Summary data
    summaryfile='C:/Users/akshay.raut/Downloads/Summary Janata 12.docx'
    summary_data = get_summary_data(summaryfile)

    # getting articles files
    articles_folder_path='C:/Users/akshay.raut/Downloads/articles_folder/'
    artilces_files=[]
    for article in os.listdir(articles_folder_path):
        artilces_files.append(article)

    # Uploading images
    images_folder_path='C:/Users/akshay.raut/Downloads/image_folder/'
    image_ids=upload_images(images_folder_path,creds)
    print('\n------------------------------------------------------------\n')

    # Adding authors
    authors_list = get_authors_list(summary_data)
    authors_ids= add_authors(authors_list,creds)
    print('\n------------------------------------------------------------\n')

    # initializing publish date
    publish_date='2020-7-19'
    publish_time_hour='1'

    posts_created=[]
    posts_not_created=[]

    if image_ids and authors_ids:

        for i in range(len(artilces_files)):

            artilce_path=articles_folder_path+artilces_files[i]
            with open(artilce_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                article_content = result.value


            publish_min=str(summary_data[i]['article_number'])   
            date_str=publish_date+'T'+publish_time_hour+':'+publish_min+':00'
            article_date=datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%S')  

            article_title = summary_data[i]['article_title']
            article_exerpt = summary_data[i]['article_exerpt']
            article_slug = article_title
            article_image_id=image_ids[i]
            article_author_id=authors_ids[i]

            data={
                    'status':'draft',
                    'title' : article_title,
                    'content' : article_content,
                    'slug': article_slug,
                    'excerpt' : article_exerpt,
                    'featured_media':article_image_id,
                    'author': article_author_id,
                    'date': article_date
                }

            create_post_status = create_post(data,creds)

            if create_post:
                posts_created.append(article_title)
            else:
                posts_not_created.append(article_title)

        print('\n------------------------------------------------------------\n')
        print('Posts created for '+ str(len(posts_created)) +' articles :')
        for i in range(len(posts_created)):
            print(str(i+1)+'. '+posts_created[i])
        print('\n------------------------------------------------------------\n')

        if len(posts_created)==len(artilces_files):
            print('Posts created for all the articles!')
        else:
            print('Posts could not be created for '+ str(len(posts_not_created)) +' articles :')
            for i in range(len(posts_not_created)):
                print(str(i+1)+'. '+posts_not_created[i])

