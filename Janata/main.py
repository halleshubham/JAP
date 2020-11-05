from GeneralSummaryWithCreds import get_summary_data
from Whatsapp.AllArticlesWhatsappByParts import whatsapp_Articles_By_Part
from Whatsapp.EnglishWhatsappMessagesUsingDOcx import LokayatEnglishWhatsapp

from Facebook.TestingWIthFRidaysForFuture import publishingAllArticles
from Facebook.FacebookTextDocx import get_Facebook_Txt_For_Kedar

import json

 #108144264067982
 #319140888763658

#f=open('jap_conf.json',"r")

creds_path="For FB.json"
with open(creds_path, encoding='utf-8-sig')  as f:
        creds=json.load(f)

summary = get_summary_data(creds["File_path"])

publishing_articles_on_FB = publishingAllArticles(creds["dates"],creds["graph_Page_ID"],creds["graph_API_Key"],summary,creds["YesDeletePosts"])

getting_All_Articles_For_Janata_Whatsapp_By_Parts=whatsapp_Articles_By_Part(summary)

getting_Facebook_Txt_For_Kedar = get_Facebook_Txt_For_Kedar(summary)

getting_Lokayat_English_Messages = LokayatEnglishWhatsapp(summary)