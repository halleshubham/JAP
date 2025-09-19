def generate_newsletter(summary, publish_date, print_edition_articles, volume_number, issue_number):

    html_section_one_init = init_html + generate_about_janata(publish_date, volume_number, issue_number) + janata_diclaimer + appeal_forward_janatweekly
    print_data = []
    blog_data = []

    for item in summary:
        if int(item['article_number']) in range(print_edition_articles[0], print_edition_articles[1]+1):
            print_data.append(item)
        else:
            blog_data.append(item)


    print_length = len(print_data)
    blog_length = len(blog_data)

    html_section_two_print_cover = ''
    html_section_three_print_articles = ''
    if print_length > 0:
        html_section_two_print_cover = generate_cover_article(print_data[0], "Print Issue")
        html_section_two_print_cover += appeal_join_janatweekly 
        html_section_three_print_articles = generate_articles(print_data[1:], print_length-1)
    
    html_section_four_blog_cover = ''
    html_section_five_blog_articles = ''

    if blog_length > 0: 
        html_section_four_blog_cover = generate_cover_article(blog_data[0], "Blog")
        if print_length == 0:
            html_section_four_blog_cover += appeal_join_janatweekly 
        html_section_five_blog_articles = generate_articles(blog_data[1:], blog_length-1)

    html_section_six_end = footer_janata + end_of_html

    final_html = html_section_one_init + html_section_two_print_cover + html_section_three_print_articles + html_section_four_blog_cover + html_section_five_blog_articles + html_section_six_end

    f = open("Newsletter.html","w",encoding="UTF-8")
    f.write(final_html)
    f.close()


def generate_internal_article(data):
	return '''<td class="column p-1" width="290" valign="top">
                                <table>
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <div class="hero-unit">
                                                    <div id="cover-image">
                                                        <a href="''' + data['article_data']["link"]  + '''">
                                                            <img class="img-fluid" src="''' + data['article_data']["jetpack_featured_media_url"] + '''" />
                                                        </a>
                                                    </div>
                                                    <div class="mt-1">
                                                        <h5>''' + data['article_data']["title"]["rendered"] + '''</h5>
                                                    </div>
                                                    <div style="color:#ED00D1;" class="mt-1">
                                                        <h6>by
                                                            <b>
                                                                <i>''' + data["article_author"] + '''</i>
                                                            </b>
                                                        </h6>
                                                    </div>
                                                    <div class="mt-1">
                                                        <p>
                                                            <p>''' + data['article_data']["excerpt"]["rendered"] + ''' </p>
                                                        </p>
                                                    </div>
                                                    <div style = "margin-top:10px">
                                                        <a href="''' + data['article_data']["link"] + '''">
                                                            <button type="button" class="btn" style="background-color:#ED00D1; color:#FFF">Read full article</button>
                                                        </a>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>'''

def generate_about_janata(publish_date, volume_number, issue_number):
    return '''<!-- Header image -->
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
                                                            <b>Vol. '''+ volume_number +''', No. ''' + issue_number + ''' | ''' + publish_date.strftime('%d %B %Y') + ''' Issue</b>
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

def generate_cover_article(data,category):
    return '''
	<!--COVER ARTICLE-->
                    <table class="section header" cellpadding="0" cellspacing="0" width="600">
                      <tr>
                            <td class="column"  align="center">
                                <br>
                                <h3 style="box-sizing:border-box;margin:0px;font-weight:500;line-height:1.6;font-size:1.75rem;background:yellow">''' + category + '''</h3>
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
                                                            <a href="''' + data['article_data']["link"] + '''">
                                                                <img class="img-fluid" src="''' + data['article_data']["jetpack_featured_media_url"] + '''"
                                                                />
                                                            </a>
                                                        </div>
                                                        <div class="mt-1">
                                                            <h3>''' + data['article_data']["title"]["rendered"] + '''</h3>
                                                        </div>
                                                        <div style="color:#ED00D1;" class="mt-1">
                                                            <h5>by
                                                                <b>
                                                                    <i>''' +data["article_author"] + '''</i>
                                                                </b>
                                                            </h5>
                                                        </div>
                                                        <div class="mt-1">
                                                            <p>
                                                                <p>''' + data['article_data']["excerpt"]["rendered"] + '''</p>
                                                            </p>
                                                        </div>
                                                        <div style = "margin-bottom:15px ; margin-top:10px">
                                                            <a href="''' + data['article_data']["link"] + '''">
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

def generate_articles(data, length):
    html = ''' '''
    for i in range(0,length):     
            if ((i+1) % 2) == 1:
                html += '''	<!-- Two columns -->
                    <table class="section mt-3" cellpadding="0" cellspacing="0">
                        <tr>'''

            html += generate_internal_article(data[i])

            if ((i+1) % 2) == 0 or i == (length - 1):
                html += ''' </tr>
                    </table>'''
  
    return html 

init_html =  '''
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

appeal_forward_janatweekly = '''<!-- Forward Janata -->
                   <table class="section header" cellpadding="0" cellspacing="0" width="600" style="background: rgb(84,27,60);margin-top:20px" >
							<tr>
								<td class="column" >
									<p  align="center" style="color: rgb(237,235,235); margin:10px; font-size:1.2rem">
										Help us increase our readership. If you are enjoying reading Janata Weekly, DO FORWARD THE MAGAZINE to your mailing list and invite people to subscribe to the weekly - for free.
									</p>
								</td>   
							</tr>				
						</table>
'''

janata_diclaimer = '''<!-- Janata Disclaimer -->
                <table class="section header" cellpadding="0" cellspacing="0" width="600" style="background: rgb(237,235,235);">
							<tr>
								<td class="column" >
									<p  align="center" style="color: rgb(84,27,60); margin:10px">
										<i  >Janata Weekly does not necessarily adhere to all of the views conveyed in articles republished by it. Our goal is to share a variety of democratic socialist perspectives that we think our readers will find interesting or useful. —Eds.</i>
									</p>
								</td>   
							</tr>				
						</table>  '''

appeal_join_janatweekly = '''<!-- Join Janata -->
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
                                                                        <img class="img-fluid float-right" src="https://janataweekly.org/wp-content/uploads/2021/11/Single_Tap.png" />
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
                                                            <div style="margin-bottom: 10px; margin-top: 15px;">
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

contribute_appeal = '''<!-- Contribute Janata -->
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

footer_janata = '''
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
                                                            <h5>
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

end_of_html = '''
                </td>
            </tr>
        </tbody>
    </table>
</body>

</html>'''






