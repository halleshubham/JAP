import pywhatkit as kit
import docx

document = docx.Document("E:/Lok/Janata/#NationaliseHealthCare-Tweets.docx")
fileData =[]
paragraph = (document.paragraphs)

a=[]
str = ''
tweets=[]

for para in paragraph:
    if ((para.text == '') and (a!=[])):
        for i in a:
            if (i!='') and (i!=a[-1]):
                str = str + i+"\n"
            if (i==a[-1]):
                str = str + i

        if (str != '') and (str != '#NationaliseHealthCare'):
            if '#NationaliseHealthCare' not in str:
                str = str + '\n#NationaliseHealthCare'
            tweets.append(str)

        print (str+"\n\n")
        str =''
        a=[]
    else:
        a.append(para.text)
#status = api.PostUpdate('I love python-twitter!')
t=10
tweetNumber=0

kit.add_driver_path('C:/Users/uday.deshmukh/Downloads/chromedriver_win32/chromedriver')
kit.load_QRcode()
b=4

for i in range(0,10):
    kit.sendwhatmsg("+919011590718", "I love studytonight.com!", 2,int(b))
    tweetNumber += 1
    a += 2
print ("Number of tweets is: ",len(tweets))
print ("Cool")



