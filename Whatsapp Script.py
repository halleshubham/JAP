from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
import docx

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
driver.get('https://web.whatsapp.com/')

#name = input('Enter the name of user or group : ')
#msg = input('Enter your message : ')
#count = int(input('Enter the count : '))

input('Enter anything after scanning QR code')

user = driver.find_element_by_xpath('//span[@title = "L Kalyani Tai"]')
user.click()

msg_box = driver.find_element_by_class_name('_3uMse')

for i in range(5):
    msg_box.send_keys(tweets[i])
    time.sleep(5)
    send_button = driver.find_element_by_css_selector('a.button.button--simple.button--primary')
    send_button.click() 

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