import docx
import os
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from GeneralSummaryWithCreds import get_summary_data

def editWordpressArticles(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            articlePath = directory+"\\"+filename
            article = docx.Document(articlePath)
            for para in article.paragraphs:
                if para.paragraph_format.right_indent != object:                
                    print ('write code for right indent')

directory = 'E:\Lok\Janata\9 August Janata'
editWordpressArticles(directory)




