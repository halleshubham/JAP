from JAP_Authentication.authenticate import get_creds
import json
from pprint import pprint
import os
from utility_functions.jap import upload_images,get_summary_data,get_authors_list,add_authors,create_post,delete_images
from datetime import datetime
import mammoth
import os,docx
import re
from docx.shared import Pt,Cm
from bs4 import BeautifulSoup

def checkIfAnyElementIsToBeRemoved(tag,title,author):
    if (tag.text == '' and (tag.img == None)):
        nextTag = tag.find_next_sibling('p')
        tag.decompose()
        tag = checkIfAnyElementIsToBeRemoved(nextTag,title,author)
    return tag

def getMatchingSoupElementWithParaText(para,soupElement):

    while (para.text.strip() != soupElement.text.strip()):
        #if (soupElement.tr != None):
        #    soupElement = soupElement.next_sibling
        #    return soupElement
        if (soupElement.li != None):
            while (para.text not in soupElement.text):
                soupElement = soupElement.next_sibling
            return soupElement

        if ('http' in soupElement.text):
            try:
                linkText =  soupElement.text.split(' http')[0]
                if (linkText in para.text):
                    break
            except:
                print ("soup Element doesn't contain http element not in para.text:",para.text)

        soupElement = soupElement.next_sibling
        if(soupElement.tr != None):
            break
    return soupElement

def convertDocxToHtml (docxFilePath,summaryOfArticle):
    title = summaryOfArticle["article_title"]
    title = title.lower()
    title = title.replace(' ','')

    author = summaryOfArticle["article_author"]
    author = author.lower()
    author = author.replace(' ','')

    article = docx.Document(docxFilePath)
    html = ''
    with open(docxFilePath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        article_content = result.value
        with open("file.html", "w", encoding="utf-8") as file:
            file.write(article_content)
    article_content = article_content.replace('\xad', '')
    article_content = article_content.replace('\u00ad', '')
    article_content = article_content.replace('\N{SOFT HYPHEN}', '')
    soup = BeautifulSoup(article_content,'html.parser')
    bullet =''
    count = 0
    countofH2 =0
    cool = soup.contents[0]
    try:
        for para in article.paragraphs:
            if (para.text != '' and (para.text != ' ' and (para.text != '\n' and (para.text != '')))):
                #cool = soup.find('p',text = para.text)
                try:
                    cool = getMatchingSoupElementWithParaText(para, cool)            
                    if (type(cool)== type(None)):
                        cool = soup.find_all('p')[count-countofH2]
                    #if (cool.text ==''):
                    #    cool.decompose()
                    #    cool = soup.find_all('p')[count-countofH2]
                    compareSoupString = str(cool.text)
                    compareSoupString =compareSoupString.lower()
                    compareSoupString = compareSoupString.replace(' ','')
                    if (title == compareSoupString):
                        coolUpdate = cool.nextSibling
                        cool.decompose()
                        cool = coolUpdate
                        continue

                    if (author == compareSoupString):
                        coolUpdate = cool.nextSibling
                        cool.decompose()
                        cool = coolUpdate
                        continue

                    cool = checkIfAnyElementIsToBeRemoved(cool,title,author)
                    #if (count == 4):
                    #    print("wait")

                    #Commenting out code for now
                    if ((cool.tr != None)):
                        print ("Article with title:\n",summaryOfArticle["article_title"],"\nhas a table. We need to manually copy the table.\n\n")
                    
                        continue

                    if ((cool.li != None) and (para.text in cool.text)):
                        #print ("Text is a bullet list so checking if ",para.text,"is present in ",cool.text,"\n\n")
                        continue

                    if ('http' in cool.text):
                        #print ("Text contains http so checking if ",para.text,"is present in ",cool.text,"\n\n")
                        continue

                    if (cool.img != None):
                        #print("Image element found \n",para.text,"\n")
                        count+=1
                        #cool = soup.find_all('p')[count-countofH2]
                        if (cool.text == None):
                            cool = cool.nextSibling

                    if (cool.text == para.text or (cool.text.strip() == para.text.strip())):
                        #print ("Text match with each other\n count will go to ",count,"+1",para.text,"\n\n")
                        count += 1

                        if (para.paragraph_format.left_indent != None or (len (para.text) - len(cool.text.strip()) >2)):
                            #print ("We have indentation for\n",para.text,"\n")
                            cool['style'] = "padding-left: 40px;"
                        if para.runs[0].font.size == Pt(14):
                    
                            #print ("Initial count of p tags is ",len(soup.find_all('p')),"\n")
                            cool.name = 'h2'
                            #print ("Updated count of p tags is ",len(soup.find_all('p')),"\n\n")
                            countofH2 +=1
                        if para.runs[0].font.underline == True:
                            newTagUnderline = soup.new_tag("span",style="text-decoration: underline;")
                            cool.insert(1,newTagUnderline)
                        if para.alignment == 1:
                            cool['class'] = "has-text-align-center"
                        elif para.alignment == 2:
                            cool['class'] = "has-text-align-right"
                    else:
                        print ("Text DO NOT match with each other\n Para.text is ",para.text,"\nCool.text is",cool.text,"\n It's title is:\n",title,"\n\n")
                except Exception as e:
                    print (e)
                    print ("\n\nBelow text is giving some error\n\n")
                    print (para.text)

    except Exception as e:
                    print (e)
                    print ("\n\nBelow text is giving some error\n\n")
                    print (para.text)
    for imageElement in soup.find_all('img'):
        imageElement['class'] = "aligncenter"
    return str(soup)

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
    print('\n------------------------------------------------------------\n')


    if 1:
        # Uploading images
        images_folder_path = params['images_folder_path']
        
        # initializing publish date
        publish_date = params['publish_date']
        publish_time_hour='1'

        posts_created=[]
        posts_not_created=[]

        if 1:
            print_edition_articles = params["print_edition_articles"]
            blog_edition_articles = params["blog_edition_articles"]
            print('\n------------------------------------------------------------\n')
            for i in range(len(artilces_files)):
                try:
                    artilce_path=articles_folder_path+artilces_files[str(int(i)+1)]
                    try:
                        article_content = convertDocxToHtml(artilce_path, summary_data[i])

                    except Exception as e:
                        print('There is some issue with getting Html From Beautiful Soup')
                        posts_not_created.append(artilce_path)
                        break

                    total_articles = len(summary_data)
                    publish_min=str((total_articles + 1) - int(summary_data[i]['article_number']))   #for publishing the articles in reverse order
                    date_str=publish_date+'T'+publish_time_hour+':'+publish_min+':00'
                    article_date=datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%S')  

                    article_title = summary_data[i]['article_title']

                    article_exerpt = summary_data[i]['article_exerpt']
                    article_slug = article_title

                    if (i+1) >= print_edition_articles[0] and (i+1) <= print_edition_articles[1]:
                        print("category for artice : " +str(i+1)+" "+str(print_edition_articles[0]))
                        categories = "669" #id for published category
                    elif (i+1) >= blog_edition_articles[0] and (i+1) <= blog_edition_articles[1]:
                        categories = "521" #id for blog category
                    else: 
                        categories = "521" 

                    #Commenting out the below publishing data as not to allow the article to publish

                    #data={
                    #        'status':'draft',
                    #        'title' : article_title,
                    #        'content' : article_content,
                    #        'slug': article_slug,
                    #        'excerpt' : article_exerpt,
                    #        'date': article_date,
                    #        'categories' : categories
                    #    }

                    #create_post_status = create_post(data,creds)

                    if create_post:
                        posts_created.append(article_title)
                    else:
                        posts_not_created.append(article_title)
                    
                except Exception as e:
                    print(e)
                    print("Could not create the draft for the article "+article_title)
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
            print('Replaced code regarding deleting dictionaries')
    else:
        print("Unable to create all the authors! Script stopped.")
                
