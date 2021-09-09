import http.client
import json
import datetime
import re


creds_path="For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds=json.load(f)
issue_date = '2021-09-05'

conn = http.client.HTTPSConnection("janataweekly.org")
   
headers = {
	'content-type': "application/json",
	'cache-control': "no-cache"
	}

#Print Issue Data
conn.request("GET", "/wp-json/wp/v2/posts?per_page=40&categories=669&after="+ issue_date +"T00:00:00")
res = conn.getresponse()
print_data = json.loads(res.read())

#Blog Issue Data
conn.request("GET", "/wp-json/wp/v2/posts?per_page=40&categories=521&after="+ issue_date +"T00:00:00")
res1 = conn.getresponse()
blog_data = json.loads(res1.read())

def getAuthorName(id):
	conn = http.client.HTTPSConnection("janataweekly.org")

	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache"
		}

	conn.request("GET", "/wp-json/wp/v2/users/"+str(id))
	res = conn.getresponse()
	data = json.loads(res.read())
	return data["name"]

def renderInternalArticle(data):
	internalArticle = '''<td class="column p-1" width="290" valign="top">
                                <table>
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <div class="hero-unit">
                                                    <div id="cover-image">
                                                        <a href="'''+data["link"]+'''">
                                                            <img class="img-fluid" src="'''+data["jetpack_featured_media_url"]+'''" />
                                                        </a>
                                                    </div>
                                                    <div class="mt-1">
                                                        <h5>'''+data["title"]["rendered"]+'''</h5>
                                                    </div>
                                                    <div style="color:#ED00D1;" class="mt-1">
                                                        <h6>by
                                                            <b>
                                                                <i>'''+getAuthorName(data["author"])+'''</i>
                                                            </b>
                                                        </h6>
                                                    </div>
                                                    <div class="mt-1">
                                                        <p>
                                                            <p>'''+data["excerpt"]["rendered"]+''' </p>
                                                        </p>
                                                    </div>
                                                    <div>
                                                        <a href="'''+data["link"]+'''">
                                                            <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">Read full article</button>
                                                        </a>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>'''
	return internalArticle




refDateObj = datetime.datetime.strptime(blog_data[0]["date"],'%Y-%m-%dT%H:%M:%S')

strF = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>
        Janata Weekly, India's oldest Socialist Weekly!
    </title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
        crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
        crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap" rel="stylesheet">
    <style>
        /* A simple css reset */

        body {
            font-family: Georgia, Times, Arial, sans-serif, cursive;
        }

        body,
        table,
        thead,
        tbody,
        tr,
        td,
        img {
            padding: 0;
            margin: 0;
            border: none;
            border-spacing: 0px;
            border-collapse: collapse;
            vertical-align: top;
        }

        /* Add some padding for small screens */

        .wrapper {
            padding-left: 10px;
            padding-right: 10px;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6,
        p {
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }

        img {
            width: 100%;
            display: block;
        }

        @media only screen and (max-width: 620px) {

            .wrapper .section {
                width: 100%;
            }

            .wrapper .column {
                width: 100%;
                display: block;
            }
        }
    </style>
</head>

<body>
    <table width="100%">
        <tbody>
            <tr>
                <td class="wrapper" width="600" align="center">'''

aboutJanata = '''<!-- Header image -->
                    <table class="section header" cellpadding="0" cellspacing="0" width="600">
                        <tr>
                            <td class="column">
                                <table>
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <div class="text-center">
                                                    <h1>
                                                        <div style="font-family: 'Alfa Slab One', Georgia, Times, Arial, sans-serif; color:#ED00D1; font-size:150%">
                                                            <b>Janata Weekly</b>
                                                        </div>
                                                    </h1>
                                                    <h3>India's oldest Socialist Weekly!</h3>
                                                    <p>
                                                        <b>Vol. 75, No. '''+ str(datetime.date.today().isocalendar()[1] - 4) +''' | '''+refDateObj.strftime('%d %B %Y')+''' Issue</b>
                                                        <br/> <font style="color:red;">Editor: </font><b>Dr. G.G. Parikh</b> | <font style="color:red;">Associate Editor: </font><b>Neeraj Jain</b> | <font style="color:red;">Managing Editor: </font><b>Guddi</b>
                                                    </p>
                                                    <hr>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>'''

def renderCoverArticle(data,category):
    coverArticle = '''
	<!--COVER ARTICLE-->
                    <table class="section header" cellpadding="0" cellspacing="0" width="600">
                      <tr>
                            <td class="column"  align="center">
                                <br>
                                <h3 style="box-sizing:border-box;margin:0px;font-weight:500;line-height:1.6;font-size:1.75rem;background:yellow">'''+ category +'''</h3>
                                <br>
                            </td>   
                        </tr>
                        <tr>
                            <td class="column">
                                <table>
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <div class="col-sm text-center">
                                                    <div class="hero-unit">
                                                        <div id="cover-image">
                                                            <a href="'''+data["link"]+'''">
                                                                <img class="img-fluid" src="'''+data["jetpack_featured_media_url"]+'''"
                                                                />
                                                            </a>
                                                        </div>
                                                        <div class="mt-1">
                                                            <h3>'''+data["title"]["rendered"]+'''</h3>
                                                        </div>
                                                        <div style="color:#ED00D1;" class="mt-1">
                                                            <h5>by
                                                                <b>
                                                                    <i>'''+getAuthorName(data["author"])+'''</i>
                                                                </b>
                                                            </h5>
                                                        </div>
                                                        <div class="mt-1">
                                                            <p>
                                                                <p>'''+data["excerpt"]["rendered"]+'''</p>
                                                            </p>
                                                        </div>
                                                        <div>
                                                            <a href="'''+data["link"]+'''">
                                                                <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">Read full article</button>
                                                            </a>
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>'''
    return coverArticle

footerJanata = '''
  <!--FOOTER-->
                    <table class="section header" cellpadding="0" cellspacing="0" width="600">
                        <tr>
                            <td class="column">
                                <table>
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <hr>
                                                <div class="row mt-3 ">
                                                    <div class="row">
                                                        <div class="col-sm-6">
                                                            <div class="hero-unit">
                                                                <div id="cover-image">
                                                                    <a href="https://www.facebook.com/JanataWeekly">
                                                                        <img style="max-width:15%" class="img-fluid img-responsive" src="https://toppng.com/public/uploads/preview/facebook-icon-facebook-icon-red-11563140071g3x2ama4cd.png"
                                                                        />
                                                                    </a>
                                                                </div>
                                                                <div style="color:#ED00D1;" class="mt-4">
                                                                    <h6>Follow us on
                                                                        <b>
                                                                            <i>Facebook</i>
                                                                        </b>
                                                                    </h6>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-6">
                                                            <div class="hero-unit">
                                                                <div id="cover-image">
                                                                    <a href="https://chat.whatsapp.com/invite/GFy7sR6uV9bD9gt5dlhE7D">
                                                                        <img style="max-width:20%" class="img-fluid img-responsive" src="https://pluspng.com/img-png/whatsapp-png-whatsapp-logo-png-1000.png"
                                                                        />
                                                                    </a>
                                                                </div>
                                                                <div style="color:#ED00D1;" class="mt-1">
                                                                    <h6>Join us on
                                                                        <b>
                                                                            <i>WhatsApp</i>
                                                                        </b>
                                                                    </h6>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>

                                                <div class="row  mt-3">
                                                    <!-- FOOTER -->
                                                    <div class="col">
                                                        <div class="hero-unit">
                                                            <div id="mail-image">
                                                                <a href="https://janataweekly.org/subscribe">
                                                                    <img class="img-fluid img-responsive" style="max-width:8%" src="https://toppng.com/uploads/preview/icon-mail-png-transparent-background-mail-logo-11562851894ksatrtd2da.png"
                                                                    />
                                                                </a>
                                                            </div>
                                                            <h5>Subscribe to Janata Weekly Hard Copy
                                                                <br/> Annual Rs. 260 | Three Years : Rs. 750
                                                                <br/> Contact: Guddi +91 7738082170
                                                                <a href="https://janataweekly.org/subscribe"> <br/> <b> Click here to <font style="{color:red;}">Receive Janata Weekly on WhatsApp & Email!</font> </a></h5>
                                                            <hr>
                                                            <h5>
                                                                <a href="http://janataweekly.org" style="color:#ED00D1;"><font style="{color:red;}">Website: </font>JanataWeekly.org</a>
                                                            </h5>
                                                        </div>
                                                    </div>

                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>
'''

endOfHTML = '''
                </td>
            </tr>
        </tbody>
    </table>
</body>

</html>'''

strF += aboutJanata

appealJoinJanatWeekly = '''<!-- Join Janata -->
                    <table class="section header mt-1" cellpadding="0" cellspacing="0" width="600" style="background: yellow;">
                        <tr>
                            <td class="column">
                                <table>
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <div class="col-sm">
                                                    <div class="row mt-1">
                                                        <div class="col-sm-4">
                                                            <div class="hero-unit text-center">
                                                                <div id="cover-image">
                                                                    <a href="https://janataweekly.org/subscribe">
                                                                        <img class="img-fluid float-right" src="http://branchaweb.com/wats1010-product-page/Single_Tap.png" />
                                                                    </a>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-8 text-center">
                                                            <div class="mt-1">
                                                                <h4>Janata at your fingertips!</h4>
                                                            </div>
                                                            <div class="mt-1">
                                                                <p>Fill below form and start receiving Janata Weekly directly
                                                                    to your E-mail and WhatsApp for free!</p>
                                                            </div>
                                                            <div>
                                                                <a href="https://janataweekly.org/subscribe">
                                                                    <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">Fill Form Now!</button>
                                                                </a>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>
'''
contributeAppeal='''<!-- Contribute Janata -->
                <br>
                    <table width = "600" style="border:1px solid #ED00D1;" >
                        <tr>
                            <td style="padding: 5px;">
                            <div class="mt-1" >
                                <h4 style="color: #ED00D1;"><b>Contribute to Janata Weekly</b></h4>
                            </div>
                            </td>
                       
                                <td style="padding: 5px;">
                                    
                                        <a href="https://imjo.in/sfmrqk">
                                            <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">₹500</button>
                                        </a>
                                    
                                </td> 
                                <td style="padding: 5px;">
                                    
                                        <a href="https://imjo.in/vQZGqM">
                                            <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">₹200</button>
                                        </a>
                                    
                                </td>
                                <td style="padding: 5px;">
                                    
                                        <a href="https://imjo.in/6Xf8af">
                                            <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">₹50</button>
                                        </a>
                                    
                                </td>        
                            </tr>   
                          
                    </table>  '''

def format_articles(data,length, category, strF,coverFlag):
    for i in range(0,length):
        #print(print_data[i]["author"])
        #if (refDateObj.date() - datetime.datetime.strptime(print_data[i]["date"],'%Y-%m-%dT%H:%M:%S').date()).days <= 3:
        if coverFlag == False :
            strF += renderCoverArticle(data[i],category)
            if category == "Print Issue":
                strF += appealJoinJanatWeekly + contributeAppeal
            elif category == "Blog":
                strF += appealJoinJanatWeekly + contributeAppeal
            coverFlag = True
        else:
            if (i%2) == 1:
                strF += '''	<!-- Two columns -->
                    <table class="section mt-3" cellpadding="0" cellspacing="0">
                        <tr>'''

            strF += renderInternalArticle(data[i])

            if (i%2) == 0 or i==(length-1):
                strF += ''' </tr>
                    </table>'''
  
    return strF 


print_length = len(print_data)
blog_length = len(blog_data)
coverFlag = False
strF = format_articles(print_data, print_length, "Print Issue", strF, coverFlag)
coverFlag = False

strF = format_articles(blog_data, blog_length, "Blog", strF, coverFlag)

strF += footerJanata
strF += endOfHTML

print(strF)
f = open("Newsletter.html","w",encoding="UTF-8")
f.write(strF)
f.close()