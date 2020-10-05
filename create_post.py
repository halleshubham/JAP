from JAP_Authentication.authenticate import get_creds
import json
from pprint import pprint
import os
from jap import upload_images,get_summary_data,get_authors_list,add_authors,create_post,delete_images
from datetime import datetime
import mammoth


creds=get_creds()

if creds:

    # getting the parameters from issue_params.json
    with open('issue_params.json') as params_file:
        params = json.load(params_file)

    # getting Summary data
    summaryfile = params['summaryfile']
    summary_data = get_summary_data(summaryfile)
    
    # getting articles files
    articles_folder_path = params['articles_folder_path']
    artilces_files={}
    for article in os.listdir(articles_folder_path):
        article_number=article.split('-')[0]
        artilces_files[article_number]=article


    # Adding authors
    authors_list = get_authors_list(summary_data)
    authors_ids= add_authors(authors_list,creds)
    print('\n------------------------------------------------------------\n')


    if authors_ids:
        # Uploading images
        images_folder_path = params['images_folder_path']
        image_dict=upload_images(images_folder_path,creds,len(authors_ids))
        
        # initializing publish date
        publish_date = params['publish_date']
        publish_time_hour='1'

        posts_created=[]
        posts_not_created=[]

        if image_dict['status']:
                image_ids=image_dict['image_ids']
                print(image_ids)
                print('\n------------------------------------------------------------\n')
                for i in range(len(artilces_files)):
                    try:
                        artilce_path=articles_folder_path+artilces_files[str(int(i)+1)]
                        try:
                            with open(artilce_path, "rb") as docx_file:
                                result = mammoth.convert_to_html(docx_file)
                                article_content = result.value
                        except Exception as e:
                            print(e)


                        publish_min=str(summary_data[i]['article_number'])   
                        date_str=publish_date+'T'+publish_time_hour+':'+publish_min+':00'
                        article_date=datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%S')  

                        article_title = summary_data[i]['article_title']
                        article_exerpt = summary_data[i]['article_exerpt']
                        article_slug = article_title
                        article_image_id=image_ids[str(int(i)+1)]
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
                    
                    except Exception as e:
                        print(e)
                        print("Could not create the draft for the article "+article_title)
                        delete_images(list(image_dict['image_ids'].values()),creds)
                        posts_not_created.append(article_title)
                        break
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

           
        else:
            print(image_dict['message'])
            delete_images(list(image_dict['image_ids'].values()),creds)
    else:
        print("Unable to create all the authors! Script stopped.")
                
