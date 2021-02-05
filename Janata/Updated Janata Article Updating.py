import requests
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from docx.shared import Pt
from GeneralSummaryWithCreds import get_summary_data
import urllib
import json
import time
import os,docx
import mammoth
import re
from bs4 import BeautifulSoup

#http://www.janataweekly.org/wp-admin

def convertDocxToHtml (directory,filename):
    docxFilePath = directory+'//'+filename
    article = docx.Document(docxFilePath)
    html = ''
    with open(docxFilePath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        article_content = result.value
        with open("file.html", "w", encoding="utf-8") as file:
            file.write(article_content)
        soup = BeautifulSoup(article_content,'html.parser')
    bullet =''
    for para in article.paragraphs:
        if para.text != '' and (para.text != ' '):
            #text = ".*"+para.text+"*."
            cool = soup.find('p',text =(para.text))
            div = soup.find_all(string = para.text)
            if para.runs[0].font.size == Pt(14):
                cool.name = 'h2'
            if para.runs[0].font.underline == True:
                newTagUnderline = soup.new_tag("span",style="text-decoration: underline;")
                cool.insert(1,newTagUnderline)
            if para.alignment == 1:
                cool['class'] = "has-text-align-center"
            elif para.alignment == 2:
                cool['class'] = "has-text-align-right"
    return soup

def editWordpressArticles(directory,summary,userName,pass1word):
    count = 0
        
    #driver =  webdriver.Chrome(ChromeDriverManager().install()) 
    ##driver = webdriver.Firefox(executable_path='E:\Lok\geckodriver.exe') 
    ##webdriver.Firefox
    #driver.get('http://www.janataweekly.org/wp-admin')
    #options = Options()
    #options.add_argument("--disable-notifications")        
    #print ('write code for right indent')
    
    ##//*[@id="user_login"]
    ##//*[@id="user_pass"]

    #try:
    #    username = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="user_login"]')))
    #    username.send_keys(userName)
    #except Exception as e: 
    #    print(e)
    #    print ("There is error entering the username")

    #try:
    #    password = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="user_pass"]')))
    #    password.send_keys(pass1word,Keys.ENTER)
    #except Exception as e: 
    #    print(e)
    #    print ("There is error entering the password")
    #print(' ')

    #try:
    #    postsButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menu-posts"]/a/div[3]')))
    #    postsButton.click()

    #except Exception as e: 
    #    print(e)


    for filename in os.listdir(directory):
        html = convertDocxToHtml(directory,filename)
        try:
            searchBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="post-search-input"]')))
            searchBox.click()
            articleTitle = summary[0]["titles"][count]
            count+=1
            searchBox.send_keys('New pots')
            searchButton =  WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="search-submit"]')))
            searchButton.click()
            articleLink = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'New pots')))
            articleLink.click()
            #//*[@id="post-10210"]
            #post-10644 > td.title.column-title.has-row-actions.column-primary.page-title > strong > a

        except Exception as e: 
            print(e)
            searchBox.click()
            searchBox.send_keys(filename)
        try:      
            extraDialog = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/div/div/div/div/div/div/div[1]/button')))
            extraDialog.click()
            textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'block-list-appender')))
            textBox.click()
        except Exception as e: 
            print(e)

        try:      
            addBlockButton = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@aria-label="Add block"]')))
            addBlockButton.click()
            #//*[@id="editor"]/div/div/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/div
            #time.sleep(10)

            searchBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@type="search"]')))
            searchBox.send_keys('Custom HTML')

            html = convertDocxToHtml(filename)

            addHTMLButton = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="editor"]/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div/ul/li')))
            addHTMLButton.click()

            textBoxActual = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@role="textbox"][@aria-label="Empty block; start writing or type forward slash to choose a block"]')))

            textBoxActual.send_keys(html)

            #InsertAnotherBlock = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="editor"]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/button')))
            #InsertAnotherBlock.click()

            #NewHtml =  WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="editor"]/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[1]/ul/li[3]/button')))
            #NewHtml.click()

        except Exception as e: 
            print(e)
            searchBox.click()
            searchBox.send_keys(filename)

#//*[@id="editor"]/div/div/div[1]/div/div[2]/div[1]/div[4]/div[1]/div/div/div/div[2]/div/div[2]/div/button/svg

    #//*[@id="post-search-input"]

creds_path="For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds=json.load(f)

summary = get_summary_data(creds["File_path"])
directory = "E://Lok//Janata//6 September"
a = editWordpressArticles(directory,summary,creds["WordpressUsername"],creds["WordpressPassword"])