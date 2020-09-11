def getting_Tweets():
    f = open('E:/Lok/All Tweets for Email.txt', "r",encoding='utf-8')
    #f=open("filename.txt","r",encoding='utf-8')
    b=f.readlines()
    tweets=[]
    string =''
    string1 =''
    string2=''
    a=[]
    for x in b:
        ct = len(x)
        lineCount = x.count('\n')
        spaceCount  = x.count(' ')
        if (b[-1] == x):
            for i in a:
                string2 = string2 + i
            string2 += x
            if (len(string2)>280):
                print (string2+'\n Size of above exceeded tweet is: '+str(len(string2))+' and the number in array is: '+str(len(tweets))+'\n\n')
            tweets.append(string2)
            continue
        if (lineCount+ spaceCount == len(x)):
            for i in a:
                string = string + i

            if (string != '') and (string != ' ') :
                if '#IfWeDoNotRise' not in string:
                    string = string + '\n#IfWeDoNotRise'

                
                elif (string.count('#RejectNEP2020') >= 2): 
                    countOfHashTag = string.count('#IfWeDoNotRise')
                    if (countOfHashTag >= 2):
                        print ("The below hashtag has two hashtags\n"+string)


                else:
                    if (string.endswith(" ")):
                        string = (string[:-1])

                    if (string.endswith("\n")):
                       string = (string[:-1])

                    if (string.endswith(" ")):
                        string = (string[:-1])

                    tweets.append(string)
            if (len(string)>280):
                print (string+'\n\n Size of above exceeded tweet is: '+str(len(string))+' and the number in array is: '+str(len(tweets)-1)+'\n\n')
            string1 = string + '\n'+ string1
            string=''
            a=[]
        else:
            a.append(x)
    return tweets
a = getting_Tweets()
b = a[1].replace('\n',' ')
uday=1
