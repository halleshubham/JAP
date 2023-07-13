from JAP_Utilities.summary_parser import get_summary_data
from JAP_Utilities.params_parser import get_params
from JAP_Utilities.jap import get_article_urls, get_articles_data
from Post_Publishing_Utilities.Whatsapp.janata_whatsapp_messages import generate_janata_whatsapp_messages
from Post_Publishing_Utilities.Whatsapp.lokayat_abhivyakti_messages import generate_lokayat_whatsapp_message, generate_abhivyakti_whatsapp_message
from Post_Publishing_Utilities.Newsletter.janata_newsletter import generate_newsletter
from datetime import datetime

if __name__ == '__main__':

    params = get_params()

    summary = get_summary_data(params["summaryfile"])

    print("Summary Retrieved..")
    article_titles = [item['article_title'] for item in summary]

    print("Fetching urls of the articles..")
    article_urls_list = get_article_urls(article_titles)

    if all(article_urls_list):
        article_urls_dict = dict(article_urls_list)
    

        #adding artcile urls to the summary
        for item in summary:
            item['article_url'] = article_urls_dict[item['article_title']]
    
        publish_date = datetime.strptime(params['publish_date'], '%Y-%m-%d')

        print("Generating Whatsapp messages for Janata channels..")
        generate_janata_whatsapp_messages(summary, publish_date, params["volume_number"])

        print("Generating Whatsapp messages for Lokayat channels..")
        generate_lokayat_whatsapp_message(summary)

        print("Generating Whatsapp messages for Abhivyakti channels..")
        generate_abhivyakti_whatsapp_message(summary)

        print("Fetching article data..")
        article_data_list = get_articles_data(article_titles)

        if all(article_data_list):
            article_data_dict = dict(article_data_list)

            #adding article data to the summary
            for item in summary:
                item['article_data'] = article_data_dict[item['article_title']]

            print("Generating Newsletter..")
            generate_newsletter(summary, publish_date, params["print_edition_articles"], params["volume_number"])
        else:
            print("Could not generate Newsletter.")

    else:
        print("Could not generate whatsapp messages.")