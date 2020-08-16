from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

f = open("E:/Lok/9 August tweets.txt", "r",encoding='utf-8')
#f=open("filename.txt","r",encoding='utf-8')
b=f.readlines()
tweets=[]
str =''
a=[]

for x in b:
    if (('Despite' in x)== True):
        uda = "rocks"
    if (x=="\n") or (x==' \n'):
        for i in a:
            str = str + i
        print (str)
        if (str != '') :
            if '#CorporateBhagaoKisaniBachao' not in str:
                str = str + '\n#CorporateBhagaoKisaniBachao'

                '''
            else: 
                countOfHashTag = str.count('#CorporateBhagaoKisaniBachao')
                if (countOfHashTag >= 2):
                    print ("There is some error")

                    '''
            else:
                if (str.endswith("\n")):
                    tweets.append(str[:-1])

                elif (str.endswith("\n ")):
                   tweets.append(str[:-2])
        str=''
        a=[]
    else:
        a.append(x)
#status = api.PostUpdate('I love python-twitter!')
t=10
tweetNumber=0
print ("End of tweets\n\n")


driver = webdriver.Chrome('C:/Users/uday.deshmukh/Downloads/chromedriver_win32/chromedriver') 
driver.get('https://tweetdeck.twitter.com/')

time.sleep(5)
driver.find_element_by_xpath('//a[@class="Button Button--primary block txt-size--18 txt-center"]')

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"][@type="text"]')
pass1 = driver.find_element_by_xpath('//input[@name="session[password]"][@type="password"]')

username.send_keys('deshmukhum15.mech@coep.ac.in')
pass1.send_keys('Udaymanoj@154')



logInButton = driver.find_element_by_xpath('//div[@role="button"]')
logInButton.click()
time.sleep(5)

retweetButtons = driver.find_element_by_xpath('//div[@data-testid="retweet"][@role="button"]')

for i in range(1,2):
    tweetBlock = driver.find_element_by_xpath('//div[@contenteditable="true"]')
    text = tweets[i]
    tweetBlock.send_keys(text)

    #time.sleep(5)
    wait = WebDriverWait(driver, 10) 

    try:
  # Tries to click an element
        driver.find_element_by_css_selector("button selector").click()

    except ElementClickInterceptedException:
  # If pop-up overlay appears, click the X button to close
     # Sometimes the pop-up takes time to load

        time.sleep(2)
        driver.find_element_by_css_selector("close button selector").click()

    #tweetButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))

    time.sleep(5)

uday = 1



