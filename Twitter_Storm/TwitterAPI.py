import twitter
import docx
import time
import json
from TextFilefortweets import getting_Tweets



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


tweets = getting_Tweets()

for k in range(50,len(tweets)):
    if (len(tweets[k])<=280):
        try:
            status = api.PostUpdate(tweets[k])
        except: 
            continue
        print (status)
        tweetNumber += 1

    else:
        print (tweets[k],'\n\n')
        print ("Incorrect. No of characters is:", len(tweets[k]))
        print ("Number of tweets is: ",len(tweets))

print ("Cool")




