# importing
from JAP_Utilities.summary_parser import get_summary_data
from JAP_Utilities.params_parser import get_params
from JAP_Utilities.jap import get_article_links
from Post_Publishing_Utilities.Whatsapp.janata_whatsapp_messages import generate_janata_whatsapp_messages
from Post_Publishing_Utilities.Whatsapp.lokayat_abhivyakti_messages import generate_lokayat_whatsapp_message, generate_abhivyakti_whatsapp_message
from datetime import datetime


 #108144264067982
 #319140888763658

if __name__ == '__main__':

    params = get_params()

    summary = get_summary_data(params["summaryfile"])

    print("Summary Retrieved..")
    article_titles = [item['article_title'] for item in summary]

    print("Fetching links of the articles..")
    article_links_list = get_article_links(article_titles)

    if all(article_links_list):
        links_dict = dict(article_links_list)
    

        #adding artcile links to the summary
        for item in summary:
            item['article_link'] = links_dict[item['article_title']]

        #publishing_articles_on_FB = publishingAllArticles(creds["dates"],creds["graph_Page_ID"],creds["graph_API_Key"],summary,creds["YesDeletePosts"])
        #getting_Facebook_Txt_For_Kedar = get_Facebook_Txt_For_Kedar(summary)

    
        publish_date = datetime.strptime(params['publish_date'], '%Y-%m-%d')

        print("Generating Whatsapp messages for Janata channels..")
        generate_janata_whatsapp_messages(summary,publish_date)

        print("Generating Whatsapp messages for Lokayat channels..")
        generate_lokayat_whatsapp_message(summary)

        print("Generating Whatsapp messages for Abhivyakti channels..")
        generate_abhivyakti_whatsapp_message(summary)

    else:
        print("Could not generate whatsapp messages")