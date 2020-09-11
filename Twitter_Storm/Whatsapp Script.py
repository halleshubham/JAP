from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
import docx
from TextFilefortweets import getting_Tweets

def checkIfMessageInBoxIsComplete(driver,text):
    try:
        msg_box = WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]'),text))
    except:

        msg_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
        msg_box.click()
        msg_box.send_keys(Keys.ENTER)

        latestMessageTextElement = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div/div[3]/div[7]/div/div/div/div[1]')))
        latestMessage = latestMessageTextElement.get_value()

        threeDots = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/header/div[3]/div/div[3]')))
        threeDots.click()
        # //*[@id="main"]/header/div[3]/div/div[3]/span/div/ul/li[2]/div
        selectMessageText = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/header/div[3]/div/div[3]/span/div/ul/li[2]/div')))
        selectMessageText.click()

        selectLastMessage = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div[3]/div/div/div[3]/div[10]/span/div/div')))
        selectLastMessage.click()

        deleteButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/span[2]/div/button[3]')))
        deleteButton.click()

        #//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[3]/div/div[3]/div
        deleteButtonForMe = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[3]/div/div[1]/div')))
        deleteButtonForMe.click()

        msg_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
        msg_box.send_keys(text)
        
        checkIfMessageInBoxIsComplete(driver,text)

        '''
    if (text == msg_box.get_attribute('value')):
        msg_box = WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]'),text))
        msg_box.send_keys(text)
        msg_box.clear()
        EC.text_to_be_present_in_element
        '''
    
driver = webdriver.Chrome('C:/Users/uday.deshmukh/Downloads/chromedriver_win32/chromedriver') 
driver.get('https://web.whatsapp.com/')

#name = input('Enter the name of user or group : ')
#msg = input('Enter your message : ')
#count = int(input('Enter the count : '))

user = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="Whatsapp Script Testing"]')))
user.click()

tweets = getting_Tweets()
slots = int(len(tweets)/20)

if ((len(tweets)%20) != 0):
    slots += 1

firstTweet= 0
lastTweet = 20

for j in range(0,slots):
    if (j == (slots-1)):
        lastTweet = len(tweets)

    if (lastTweet%20 == 0) or (lastTweet == len(tweets)):
        text = '*Tweets from ['+str(firstTweet)+' - '+str(lastTweet)+']* are given below'

        msg_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]')))
        msg_box.send_keys(text)
        
        checkIfMessageInBoxIsComplete(driver,text)
        text = ''
        send_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]')))
        send_button.click()

    for i in range(firstTweet,lastTweet):
        twe = tweets[i].replace('\n',' ')
        try :
            msg_box.send_keys(twe)
        except:
            print ("There is some error, manual interpretation needed")
        checkIfMessageInBoxIsComplete(driver,twe)

        try:
            send_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]')))
            send_button.click()
        except:
            print("There is some popup")

        #send_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]')))
        #send_button.click()

    firstTweet = lastTweet
    lastTweet += 20

driver = webdriver.Chrome('C:/Users/uday.deshmukh/Downloads/chromedriver_win32/chromedriver') 
  
driver.get("https://web.whatsapp.com/") 
wait = WebDriverWait(driver, 90) 
  
# Replace 'Friend's Name' with the name of your friend  
# or the name of a group  
target = '"L Mayur"'
  
# Replace the below string with your own message 
string = "Cool Bro!!!"
  
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located(( 
    By.XPATH, x_arg))) 
group_title.click() 
inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located(( 
    By.XPATH, inp_xpath))) 
for i in range(10): 
    input_box.send_keys(string + Keys.ENTER) 
    time.sleep(1) 