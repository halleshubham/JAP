f = open("E:/Lok/9 August tweets.txt", "r",encoding='utf-8')
#f=open("filename.txt","r",encoding='utf-8')
b=f.readlines()
tweets=[]
str =''
a=[]
for x in b:
    if (x=="\n"):
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
                else:
                    tweets.append(str)
        str=''
        a=[]
    else:
        a.append(x)
uday=1
