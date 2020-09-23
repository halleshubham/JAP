import requests
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from GeneralSummaryWithCreds import get_summary_data
import urllib
import json
import time

def getImages(summary):
    driver = webdriver.Chrome('C:/Users/uday.deshmukh/Downloads/chromedriver_win32/chromedriver') 
    #driver = webdriver.Firefox(executable_path='E:\Lok\geckodriver.exe') 
    #webdriver.Firefox
    driver.get('https://www.google.com/imghp')

    # get the image source

    searchTextbox = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    #//input[@title="Search"]
    searchTextbox.send_keys(summary[0]["titles"][2])
    searchButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Google Search"]')))
    searchButton.click()

    textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/c-wiz/div/header/div[2]/div/div[1]/form/div[1]/div[2]/div/div[2]/input')))
    textBox.clear()
    # download the image
    count = 1
    imagepaths = []
    for title in summary[0]["titles"]:
        textBox = driver.find_element_by_xpath('//input[@title="Search"]')
        textBox.send_keys(title)
        searchButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/c-wiz/div/header/div[2]/div/div[1]/form/div[1]/div[2]/button')))
        searchButton.click()
        

        img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]/div[1]/img')))
        img.click()

        time.sleep(10)

        try: 
            imageBiggerSize = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')))
        except: 
            img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]/div[1]/img')))
            img.click()
            imageBiggerSize = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')))
        
        classTxt = imageBiggerSize.get_attribute('class')
        forGettingLink = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,classTxt)))
        url = forGettingLink.get_attribute("src")
        imagepaths.append(url)

        #actionChains = ActionChains(driver)
        #actionChains.context_click(imageBiggerSize).perform()

        #actionChains.send_keys('v')
        #actionChains.perform()
        #actionChains.send_keys('v').perform()
        #actionChains.context_click(imageBiggerSize).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        #actionChains.context_click(imageBiggerSize).send_keys(Keys.ARROW_DOWN,Keys.RETURN)
        #actionChains.perform()
        
        #actionChains.context_click(imageBiggerSize).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        #actionChains.perform()
        
        '''
        parentGUID = driver.current_window_handle
        imageBiggerSize.click()
        #href = imageBiggerSize.get_attribute('href')
        #driver.get(href)
        time.sleep(7)
    
        allGUID = driver.window_handles

        for guid in allGUID:
            if(guid != parentGUID):
                driver.switch_to_window(guid)
                #/html/body/div[1]/div[4]/div/div[1]/article/div[1]/figure/img
                #//*[@id="post-16963"]/div[1]/figure/img
        imageWebsite = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[1]/article/div[1]/figure/img')
        src = imageWebsite.get_attribute('src')
        '''
        closeBigImage = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@aria-label="Close"]')))
        closeBigImage.click()

        textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@title="Search"]')))
        textBox.clear()
       
        try:
            resource =urllib.request.urlopen(url)
            output = open(str(count)+".jpg","wb")
            output.write(resource.read())
            output.close()
        except:
            try:
                resource =urllib.request.urlopen(url)
                outputPNG= open (str(count)+".png","wb")
                outputPNG.write(resource.read())
                outputPNG.close()
            except:
                try:
                    resource =urllib.request.urlopen(url)
                    outputjpeg= open (str(count)+".jpeg","wb")
                    outputjpeg.write(resource.read())
                    outputjpeg.close()
                except:
                    count += 1
                    continue
        count += 1
    return imagepaths

    driver.close()

creds_path="For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds=json.load(f)

summary = get_summary_data(creds["File_path"])
a = getImages(summary)
