import twitter
import docx
import time

api = twitter.Api(consumer_key='XZDZOUX85Ogarr5QYziwhiww4',
                  consumer_secret='yoLTwfI9lDoFwKCnVVBvt6WpTRD4b0YiMfU9lB0yFu8jeIHCY2',
                  access_token_key='788311789444468736-WKWKbwyrg8oycc7x9FMS54qiXInEYUx',
                  access_token_secret='cdpAVL1oLdrqL0iY0u9iyoNutaBpbWuETojBU9rA1bC7Z')

'''
follower = api.GetFollowerIDs()

postImage = api.PostUpdate(status='#NationaliseHealthCare',media='E:/Lok/Janata/8 May issue')
tweets = api.GetFavorites(user_id='1239472596544086026',count=100)
user = api.GetUser('1239472596544086026')
userTimeline = api.GetUserTimeline(screen_name='JanataWeekly',count=80)
lists = api.GetLists(user_id='1239472596544086026')
#listTimeline = api.GetListTimeline(slug=None,owner_id='1239472596544086026')
search = api.GetSearch(term='#NationaliseHealthCare',count=80)
'''


'''
for para in paragraph:
    fileData.append(para.text)

rawData="".join(fileData)
tweets = rawData.split
'''


f = open("E:/Lok/All Tweets for Email.txt", "r",encoding='utf-8')
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
                tweets.append(str)
                '''
                if (str.endswith("\n")):
                    tweets.append(str[:-1])

                elif (str.endswith("\n ")):
                   tweets.append(str[:-2])
                   '''
        str=''
        a=[]
    else:
        a.append(x)
#status = api.PostUpdate('I love python-twitter!')
t=10
tweetNumber=0
print ("End of tweets\n\n")
#status = api.PostUpdate('I love python-twitter!')
t=10
tweetNumber=0
print ("End of tweets\n\n")
for k in range(50,len(tweets)):
    if (len(tweets[k])<=280):
        status = api.PostUpdate(tweets[k])
        print (status)
        tweetNumber += 1

    else:
        print (tweets[k],'\n\n')
        print ("Incorrect. No of characters is:", len(tweets[k]))
        print ("Number of tweets is: ",len(tweets))

print ("Cool")




