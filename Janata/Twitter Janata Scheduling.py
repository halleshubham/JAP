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

def GetWeekCount (driver, date):
    try:
        scheduleButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[13]/button/span')))    
        scheduleButton.click()
    except:
        uday = "Bad boy"
        scheduleButton.click()
    try:
        for weCount in range(1,7):
            for dyCount in range(1,8):
                xpathDate = '//*[@id="calweeks"]/div['+str(weCount)+']/a['+str(dyCount)+']'
                scheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xpathDate)))
                attribute = scheduledTweetDate.get_attribute('class')
                valueDate = scheduledTweetDate.text
                if ('caldisabled' in attribute) or (valueDate != (str(date["day"]))):
                    print (date["day"],' is not matching with '+ valueDate+'\n')
                    continue
                else:
                    driver.refresh()
                    return [dyCount,weCount]
        print ("Uday")
    except Exception as e:
        print(e)
        print (type(e))

def CheckIfMonthIsCorrect(driver, date):
    try:
        tweetBlock = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')))
        tweetBlock.send_keys("Test Month is Correct or not")
    except:
        time.sleep(5)
        tweetBlock.clear()

    try:
        scheduleButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[13]/button/span')))    
        scheduleButton.click()
    except:
        uday = "Bad boy"
        scheduleButton.click()
    try:
        Month = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="caltitle"]')))    
        month = Month.text
        if (date["month"] in month):
            print ("Month is correct")
            driver.refresh()
            return False
        else:
            print ("Month is NOT correct")
            driver.refresh()
            return True
    except:
        uday = "Bad boy"
        scheduleButton.click()
    

def eachAccountTweets(userName, password,summary,date):
    author = summary[0]['authors']
    excerpt = summary[0]['excerpts']
    title = summary[0]['titles']
    l = len(author)
    time = [10, 12, 3, 6]
    eachPostTime = {}

    #nineAM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][0][0],dateTime["TwitterTimings"][0][1]]
    #elevenAM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][1][0],dateTime["TwitterTimings"][1][1]]
    #threePM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][2][0],dateTime["TwitterTimings"][3][1]]
    #sixPM = [dateTime["TwitterDates"][0],dateTime["TwitterTimings"][2][0],dateTime["TwitterTimings"][3][1]]

    dateCount = 0

    for i in range(0,l):
        if ((i+1) <= 7):
            eachPostTime[i] = time[0]
            #eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][1][0],dateTime["TwitterTimings"][1][1]]
            #elevenAM += 86400


        elif ((i+1) > 7 and (i+1) <= 14):
            eachPostTime[i] = time[1]
            #eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][2][0],dateTime["TwitterTimings"][2][1]]
            #threePM += 86400
        elif ((i+1) > 14 and (i+1) <= 21):
            eachPostTime[i] = time[2]
            #eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][3][0],dateTime["TwitterTimings"][3][1]]
            #sixPM += 86400
        else:
            eachPostTime[i] = time[3]
            #eachPostTime[i] = [dateTime["TwitterDates"][dateCount],dateTime["TwitterTimings"][0][0],dateTime["TwitterTimings"][0][1]]
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
    dayAndWeek = GetWeekCount(driver, date)
    rawDayCount = dayAndWeek[0]
    rawWeekCount = dayAndWeek[1]
    dayCount = dayAndWeek[0]
    weekCount = dayAndWeek[1]
    nextMonthClick = CheckIfMonthIsCorrect(driver, date)
    previousMonthClick = False

    while j < l:
        if (refDateObj.date() - datetime.datetime.strptime(data[j]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
            print (title[j], author[j], eachPostTime[j])
            b= author[j][-1]
            if (b == ' '):
                author[j-1] = author[j-1][:-1]

            a= excerpt[j][-1]
            if (a == ' '):
                excerpt[j-1] = excerpt[j-1][:-1]

            strF1 += title[j] + "\n\n"
            strF1 += author[j] + "\n\n"
           #+ excerpt[j] + "\n\n"
            strF1 += data[j]["link"] + "\n\n"
            
            #strF1 = getTags(data[i]["id"],strF1)
            scheduleTweetsUsingTwitterDeck1 = scheduleTweetsUsingTwitterDeck(nextMonthClick,strF1,dayCount,weekCount,eachPostTime[j],driver,date,previousMonthClick)
            print(strF1)
            dayCount += 1

            if (nextMonthClick == True):
                weekCount = 1
                dayAndWeek[1] = 1

            if (previousMonthClick == True):
                previousMonthClick = False

            if (int(scheduleTweetsUsingTwitterDeck1[0])> int(scheduleTweetsUsingTwitterDeck1[1])):
                weekCount = 1
                nextMonthClick = True
            else:
                nextMonthClick = False
            
            if(dayCount >7 ):
                dayCount =1
                weekCount += 1
                #nextMonthClick = CheckIfMonthIsCorrect(driver, date)
                #if (nextMonthClick == False):
                #    dayCount = dayAndWeek[0]
                #    weekCount = dayAndWeek[1]

                #if (nextMonthClick == True):
                #    weekCount = 1
                #    dayAndWeek[1] = 1
                
            if (int(scheduleTweetsUsingTwitterDeck1[1]) > int(date["day"]+6)):
                #nextMonthClick = CheckIfMonthIsCorrect(driver, date)
                dayCount = dayAndWeek[0]
                weekCount = dayAndWeek[1]
                
            if ((j+1)%7 == 0 and (date["day"] in [28,29,30,31])):
                #click previous month
                dayAndWeek[0] = rawDayCount
                dayAndWeek[1] = rawWeekCount
                dayCount = dayAndWeek[0]
                weekCount = dayAndWeek[1]

                previousMonthClick = True

                print ("\nPrevious  month clicked\n")

            
            print('Time is '+str(eachPostTime[j])+ '\nDate is '+(scheduleTweetsUsingTwitterDeck1[0])+'\nNext date is '+scheduleTweetsUsingTwitterDeck1[1]+'\n')
            j = j + 1
            strF1 = ''
        i = i - 1
    driver.close

def scheduleTweetsUsingTwitterDeck(nextMonthClick,tweets,dayCount,weekCount,hour,driver,date,previousMonthClick):
    
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
        scheduledTweetMinutes.send_keys(str(30))
    except:
        print("There is some error hitting hour while scheduling")
    try:

        AMOrPM = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="amPm"]')))
        AmOrPmValue = AMOrPM.text
        if (AmOrPmValue != date["timings"][str(hour)]):
            amOrPM = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="amPm"]'))) 
            amOrPM.click()
            amOrPM = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="amPm"]'))) 
            getValueOfAmOrPmChanged = amOrPM.text
            print("Expected time is ",str(hour)," ",date["timings"][str(hour)], "And has been changed to ", str(getValueOfAmOrPmChanged))
        else:
            print("Expected time is ",str(hour)," ",date["timings"][str(hour)], "And is the same")
    except Exception as e:
        print(e)
    if (nextMonthClick == True):
        try:
            nextMonth = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="next-month"]/i')))
            nextMonth.click()
            weekCount =1
        except Exception as e:
            print('There is some error while checking nexMonthCLick\n')
            print(e)
    if (previousMonthClick == True):
        try:
            clickPreviousButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="prev-month"]')))
            clickPreviousButton.click()

        except Exception as e:
            print('There is some error while clicking previousMonth\n')
            print(e)

    try:
        xpathDate = '//*[@id="calweeks"]/div['+str(weekCount)+']/a['+str(dayCount)+']'
        if ((dayCount+1)>7):
            nextxpathDate='//*[@id="calweeks"]/div['+str(weekCount+1)+']/a['+str(1)+']'
        else:
            nextxpathDate='//*[@id="calweeks"]/div['+str(weekCount)+']/a['+str(dayCount+1)+']'
        scheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xpathDate)))
        nextScheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,nextxpathDate)))
        value=[]
        value.append(scheduledTweetDate.text)
        value.append(nextScheduledTweetDate.text)
        scheduledTweetDate.click()
        scheduledTweetDate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xpathDate)))
        scheduledTweetDate.click()

    except Exception as e:
        print('There is some error while scheduling date\n')
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
        print ("Tweet block is not clear\n")
        print(e)
    return value

accountsjson = "TwitterData.json"
with open(accountsjson, encoding='utf-8-sig')  as f:
        accounts = json.load(f)

creds_path = "For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds = json.load(f)

summary = get_summary_data(creds["File_path"])
ueachAccountTweets = eachAccountTweets(accounts["Username"],accounts["Password"],summary,accounts["date"])

#7 - Uday coep
#5 - Jitu
#0 - Vishal

print('Udya rocks')
#retweetButtons =
#driver.find_element_by_xpath('//div[@data-testid="retweet"][@role="button"]')
uday = 1

#articleLink = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'New pots')))


