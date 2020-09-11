from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from TextFilefortweets import getting_Tweets
from selenium.webdriver.common.keys import Keys
import random
import json
import os

def imagesInstantly (articles_folder_path,driver):
    for image in os.listdir(articles_folder_path):
        imagePath = articles_folder_path+image
        #tweetDeckBlock = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')
        twitterTweetBlock = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]')
        twitterTweetBlock.send_keys(imagePath)
        try:
            twitterTweetBlock.send_keys(imagePath)
            continue
        except:
            print ('Uday')
        #tweetBlock.send_keys(image)
        imageBlock = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/button/span')
        tweetBlock.send_keys("E://Lok//5 September//118340940_104146234759179_530032245830299162_o.png")
        imageMiniBlock = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/div[2]')
        #time.sleep(5)
        #wait = WebDriverWait(driver, 10) 
        imageBlock.send_keys('file:///E://Lok//5%20September//118340940_104146234759179_530032245830299162_o.png')
        #imageMiniBlock.send_keys(imagePath)
        tweetBlock.send_keys('E:\\Lok\\5 September\\118340940_104146234759179_530032245830299162_o.png')
        imageBlock.send_keys(imagePath)
        #imageBlock.click()

        imageFileElement = driver.switch_to_active_element()
        
        #imagePath = articles_folder_path+image
        #imageFileElement.send_keys(imagePath)

        try:
            tweetBlock.send_keys(Keys.ENTER)
            tweetButton.click()

        except:
            tweetBlock.send_keys(Keys.ENTER)
            tweetButton.click()

            time.sleep(5)
            tweetButton.click()
        try:
            tweetBlock.clear()
        except:
            time.sleep(5)
            continue
            tweetBlock.clear()

def tweetInstantly(tweets,driver):
    
    for i in range(120,len(tweets)):
        
        tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
        text = tweets[i]
        tweetBlock.send_keys(text)
        tweetBlock.send_keys(Keys.ENTER)
        #time.sleep(5)
        #wait = WebDriverWait(driver, 10) 
        
        try:
            tweetButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[12]/div/div/button')))
            tweetButton.click()

        except:
            tweetBlock.send_keys(Keys.ENTER)
            tweetButton.click()

            time.sleep(5)
            tweetButton.click()
        try:
            tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
            tweetBlock.clear()
        except:
            time.sleep(5)
            continue
            tweetBlock.clear()
        
        
        #tweetButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))
        
def eachAccountTweets(userName, password):
    driver = webdriver.Chrome('C:/Users/uday.deshmukh/Downloads/chromedriver_win32/chromedriver') 
    driver.get('https://tweetdeck.twitter.com/')

    try:
        login = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[3]/div/div[2]/section/div[1]/a')))
        login.click()
    except:
        print ("There is some login button error")

    try:
        username = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@name="session[username_or_email]"][@type="text"]')))
        username.send_keys(userName)
    except:
        print ("There is error entering the username")

    try:
        pass1 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@name="session[password]"][@type="password"]')))
        pass1.send_keys(password)
    except:
        print ("There is error entering the password")

    try:
        logInButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@role="button"]')))
        logInButton.click()
    except:
        print ("There is some error clicking the logInButton")

    #tweetFeatherButton = driver.find_element_by_xpath('/html/body/div[3]/header/div/button')
    #tweetFeatherButton.click()

    articles_folder_path ='E:/Lok/5 September/'
    #ImageInstantly = imagesInstantly (articles_folder_path,driver)

    #scheduleTweetsUsingTwitterDeck1 = scheduleTweetsUsingTwitterDeck(tweets,8,14,5,driver)
    tweetsInstantly = tweetInstantly(tweets,driver)
    driver.close

def scheduleTweetsUsingTwitterDeck(tweets,hour,minutes,noOfTweets,driver,startingTweetNumber,EndTweetNumber):
    count = 1
    for i in range (startingTweetNumber,EndTweetNumber):
        text = tweets[i]
        try:
            tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
            tweetBlock.send_keys(text)
        except:
            time.sleep(5)
            continue
            tweetBlock.clear()

        try:
            scheduleButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[13]/button/span')))    
            scheduleButton.click()
        except:
            uday = "Bad boy"
            scheduleButton.click()

        #scheduledTweetHour.click()
        #scheduledTweetHour.send_keys('')
        
        try:
            scheduledTweetHour = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="scheduled-hour"]')))  
            scheduledTweetHour.send_keys('')
            scheduledTweetHour.send_keys('\ue003')
            scheduledTweetHour.send_keys('\ue003')
            scheduledTweetHour.send_keys(str(hour))
        except:
            print ("There is some error hitting hour while scheduling")

        try:
            scheduledTweetMinutes = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="scheduled-minute"]')))  
            scheduledTweetMinutes.send_keys('')
            scheduledTweetMinutes.send_keys('\ue003')
            scheduledTweetMinutes.send_keys('\ue003')
            scheduledTweetMinutes.send_keys(str(minutes))
        except:
            print ("There is some error hitting hour while scheduling")
            
        if (count%noOfTweets) == 0:
            minutes += 1
        if (count == 30):
            count = 1
            minutes += 8

        try:
            scheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="calcurrent"]')))  
            scheduledTweetDate.click()

        except:
            print ("There is some error hitting hour while scheduling")

        try:
            tweetButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[12]/div/div/button')))
            tweetButton.click()
        except:
            print ("There is some error hitting hour while scheduling")
        count += 1

        #tweetFeatherButton = driver.find_element_by_xpath('/html/body/div[3]/header/div/button')
        #tweetFeatherButton.click()

        try:
            tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
            tweetBlock.clear()
        except:
               continue

accountsjson="TwitterAccountsData.json"
with open(accountsjson, encoding='utf-8-sig')  as f:
        accounts=json.load(f)
tweets = getting_Tweets()

ueachAccountTweets = eachAccountTweets(accounts[0]["Username"],accounts[0]["Password"])

#7 - Uday coep
#5 - Jitu
#0 - Vishal

startingTweetNumber = 0
EndTweetNumber = len(tweets)

scheduleTweets = scheduleTweetsUsingTwitterDeck(tweets,7,5,5,driver,startingTweetNumber,EndTweetNumber)
tweetsInstantly = tweetInstantly(tweets)
print ('Udya rocks')
#retweetButtons = driver.find_element_by_xpath('//div[@data-testid="retweet"][@role="button"]')

uday = 1



