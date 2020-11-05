from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from GeneralSummaryWithCreds import get_summary_data
from selenium.webdriver.common.keys import Keys
import random
import json
import os
import http.client
import json
import datetime
import re
import unicodedata
import docx

def loginToTwitter(userName, password):
    driver = webdriver.Chrome(ChromeDriverManager().install()) 
    driver.get('https://tweetdeck.twitter.com/')

    try:
        login = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[3]/div/div[2]/section/div[1]/a')))
        login.click()
    except:
        print("There is some login button error")

    try:
        username = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@name="session[username_or_email]"][@type="text"]')))
        username.send_keys(userName)
    except:
        print("There is error entering the username")

    try:
        pass1 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@name="session[password]"][@type="password"]')))
        pass1.send_keys(password)
    except:
        print("There is error entering the password")

    try:
        logInButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@role="button"]')))
        logInButton.click()
    except:
        print("There is some error clicking the logInButton")
    return driver

def getTags(id,tweet):
	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }

	conn.request("GET", "/wp-json/wp/v2/tags?post=" + str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	tags1 = ""
	for i in data:
		tag1 = i["name"].replace(" ", "")
		tag1 = tag1.replace("-", "_")            
		tags1 += "#" + tag1
		if ((len(tweet + tag1) > 280)):
			return tweet
		else:
			tweet += tag1 + " "
		return tweet

	print(tags1)
	return (tags1)

def eachAccountTweets(userName, password,summary,dateTime):

    author = summary[0]['authors']
    excerpt = summary[0]['excerpts']
    title = summary[0]['titles']
    l = len(author)

    eachPostTime = {}

    nineAM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][0][0],dateTime["TwitterTimings"][0][1]]
    elevenAM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][1][0],dateTime["TwitterTimings"][1][1]]
    threePM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][2][0],dateTime["TwitterTimings"][3][1]]
    sixPM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][2][0],dateTime["TwitterTimings"][3][1]]
    dateCount = 0

    for i in range(l-1,-1,-1):
        if ((l - i) <= 7):
            eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][1][0],dateTime["TwitterTimings"][1][1]]
            #elevenAM += 86400


        elif ((l - i) > 7 and (l - i) <= 14):
            eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][2][0],dateTime["TwitterTimings"][2][1]]
            #threePM += 86400
        elif ((l - i) > 14 and (l - i) <= 21):
            eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][3][0],dateTime["TwitterTimings"][3][1]]
            #sixPM += 86400
        else:		
            eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][0][0],dateTime["TwitterTimings"][0][1]]
            #nineAM += 86400
        dateCount += 1
        if dateCount == 7:
            dateCount = 0

    l = len(author)
    strF1 = ''

    driver = loginToTwitter(userName,password)

    conn = http.client.HTTPSConnection("janataweekly.org")

    headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }

    conn.request("GET", "/wp-json/wp/v2/posts?per_page=30")
    res = conn.getresponse()
    data = json.loads(res.read())
    l = len(author)
    if (l >29):
        l = 29
    j = 0
    i = l
    refDateObj = datetime.datetime.strptime(data[0]["date"],'%Y-%m-%dT%H:%M:%S')
    dayCount= 1
    weekCount = 6
    while j < l:
        if (refDateObj.date() - datetime.datetime.strptime(data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
            print (title[j], author[j], eachPostTime[i])
            b= author[j-1][-1]
            if (b == ' '):
                author[j-1] = author[j-1][:-1]

            a= excerpt[j-1][-1]
            if (a == ' '):
                excerpt[j-1] = excerpt[j-1][:-1]

            strF1 += title[j] + "\n\n"
            strF1 += author[j] + "\n\n"
           #+ excerpt[j] + "\n\n"
            strF1 += data[i]["link"] + "\n\n"
            j = j + 1
            strF1 = getTags(data[i]["id"],strF1)
            scheduleTweetsUsingTwitterDeck1 = scheduleTweetsUsingTwitterDeck(strF1,dayCount,weekCount,eachPostTime[i][1],eachPostTime[i][2],driver)
            print(strF1)
            dayCount += 1
            if (scheduleTweetsUsingTwitterDeck1 == '1'):
                weekCount = 2
            if(dayCount >7):
                dayCount =1
                weekCount += 1
            
            print(scheduleTweetsUsingTwitterDeck1)
            strF1 = ''
        i = i - 1
    driver.close

def scheduleTweetsUsingTwitterDeck(tweets,dayCount,weekCount,hour,minutes,driver):
    
    try:
        tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
        tweetBlock.send_keys(tweets)
    except:
        time.sleep(5)
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
        print("There is some error hitting hour while scheduling")

    try:
        scheduledTweetMinutes = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="scheduled-minute"]')))  
        scheduledTweetMinutes.send_keys('')
        scheduledTweetMinutes.send_keys('\ue003')
        scheduledTweetMinutes.send_keys('\ue003')
        scheduledTweetMinutes.send_keys(str(minutes))
    except:
        print("There is some error hitting hour while scheduling")
    try:
        amOrPM = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="amPm"]'))) 
        PM = amOrPM.get_attribute("data-value")
        if (PM !="PM"):
            amOrPM = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="amPm"]'))) 
            amOrPM.click()
    except Exception as e:
        print(e)

    try:
        xpathDate = '//*[@id="calweeks"]/div['+str(weekCount)+']/a['+str(dayCount)+']'
        scheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xpathDate)))
        value = scheduledTweetDate.text
        scheduledTweetDate.click()
        scheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xpathDate)))
        scheduledTweetDate.click()

    except Exception as e:
        print(e)

    try:
        tweetButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[12]/div/div/button')))
        tweetButton.click()
    except:
        print("There is some error hitting hour while scheduling")
    dayCount += 1

    try:
        tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
        tweetBlock.clear()
    except Exception as e:
        print(e)
    return value

accountsjson = "TwitterAccountsData.json"
with open(accountsjson, encoding='utf-8-sig')  as f:
        accounts = json.load(f)

creds_path = "For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds = json.load(f)

summary = get_summary_data(creds["File_path"])
ueachAccountTweets = eachAccountTweets(accounts[1]["Username"],accounts[1]["Password"],summary,accounts[9])

#7 - Uday coep
#5 - Jitu
#0 - Vishal
startingTweetNumber = 0
EndTweetNumber = len(tweets)

print('Udya rocks')
#retweetButtons =
#driver.find_element_by_xpath('//div[@data-testid="retweet"][@role="button"]')
uday = 1

#articleLink = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'New pots')))


