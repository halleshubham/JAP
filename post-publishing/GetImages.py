import requests
import shutil
from webdriver_manager.chrome import ChromeDriverManager
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
import wget

def getAnotherImage(title,driver):
    textBox = driver.find_element_by_xpath('//input[@title="Search"]')
    textBox.send_keys(title)
    searchButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/c-wiz/div/header/div[2]/div/div[1]/form/div[1]/div[2]/button')))
    searchButton.click()

    img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/a[1]/div[1]/img')))
    img.click()

    time.sleep(10)

    try: 
        imageBiggerSize = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')))
    except Exception as e:
        print (e)
        img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="islrg"]/div[1]/div[2]/a[1]/div[1]/img')))
        img.click()
        imageBiggerSize = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')))
        
    classTxt = imageBiggerSize.get_attribute('class')
    try:
        forGettingLink = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,classTxt)))
    except Exception as e:
        print (e)
        closeBigImage = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@aria-label="Close"]')))
        closeBigImage.click()

        textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@title="Search"]')))
        textBox.clear()
        return e
        
    url = forGettingLink.get_attribute("src")
    imagepaths.append(url)

    closeBigImage = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@aria-label="Close"]')))
    closeBigImage.click()

    textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@title="Search"]')))
    textBox.clear()
       
    try:
        image_file = wget.download(url)
        resource =urllib.request.urlopen(url)
        output = open(str(count)+".jpg","wb")
        output.write(resource.read())
        output.close()
    except Exception as e:
        print (e)
        try:
            resource =urllib.request.urlopen(url)
            outputPNG= open (str(count)+".png","wb")
            outputPNG.write(resource.read())
            outputPNG.close()
        except Exception as e:
            print (e)
    return resource

def getImages(summary):
    driver = webdriver.Chrome(ChromeDriverManager().install()) 
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
    for i in range(0,len(summary[0]["titles"])):
        searchAuthor = summary[0]["authors"][i]
        if (';' in searchAuthor):
            searchAuthor = searchAuthor.split(';',1)
            searchAuthor = searchAuthor[0]
        if (',' in searchAuthor):
            searchAuthor = searchAuthor.split(',',1)
            searchAuthor = searchAuthor[0]

        searchTitle = summary[0]["titles"][i]
        if ('Two' in searchTitle):
            searchTitle = searchTitle.split('Two',1)
            searchTitle = searchTitle[0]

        textBox = driver.find_element_by_xpath('//input[@title="Search"]')
        searchText = searchTitle + " " + searchAuthor
        textBox.send_keys(searchText)
        searchButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/c-wiz/div/header/div[2]/div/div[1]/form/div[1]/div[2]/button')))
        searchButton.click()

        try:
            img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img')))
            img.click()
        except Exception as e:

            textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@title="Search"]')))
            textBox.clear()
            count += 1
            continue

        time.sleep(10)

        try: 
            imageBiggerSize = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')))
        except Exception as e:
            print (e)
            img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]/div[1]/img')))
            img.click()
            imageBiggerSize = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')))
        
        classTxt = imageBiggerSize.get_attribute('class')
        forGettingLink = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,classTxt)))
        url = forGettingLink.get_attribute("src")
        imagepaths.append(url)

        closeBigImage = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@aria-label="Close"]')))
        closeBigImage.click()

        textBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@title="Search"]')))
        textBox.clear()
       
        try:
            resource =urllib.request.urlopen(url, timeout=20)
            output = open(str(count)+".jpg","wb")
            output.write(resource.read())
            output.close()
        except Exception as e:
            print (e)
            image_url = url
            #try:
            #    image_file = wget.download(url)
            #except Exception as e:
            #    print (e)
            filename = str(count)+".jpeg"
            try:

            # Open the url image, set stream to True, this will return the stream content.
                r = requests.get(image_url, stream = True,timeout = 15)

                # Check if the image was retrieved successfully
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True
    
                    # Open a local file with wb ( write binary ) permission.
                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r.raw, f)
        
                    print('Image sucessfully Downloaded: ',filename)
            except Exception as e:
                print(e, 'Image Couldn\'t be retreived\n')

        count += 1
    return imagepaths

    driver.close()

creds_path="For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds=json.load(f)

summary = get_summary_data(creds["File_path"])
a = getImages(summary)
