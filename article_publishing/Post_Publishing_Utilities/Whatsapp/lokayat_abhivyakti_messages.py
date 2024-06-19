def generate_lokayat_whatsapp_message(summary):

	total_articles_count = len(summary)

	message_separator = "********************* New Message Starts Here *********************\n\n"

	message_section_two = "-----------------------------------------------------------\n 📱 _Join Lokayat's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/DxY7U42lGBeHyLJwUYCtn4\n\n"
	message_section_two += "📱 _लोकायतचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/DQtYRIIuydR2fMTjTHVcOT\n\n"
	message_section_two += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"

	message_section_one = ""
	file = open("EnglishWhatsappMessagesWithLokayatFooter.txt","w",encoding="UTF-8")
	for i in range(0,total_articles_count):
		message_section_one = "⭕ *"+summary[i]['article_title'].strip()+"*\n\n"
		message_section_one += "✒️ "+summary[i]['article_author']+"\n\n_"+summary[i]['article_excerpt'].strip()+"_\n\n*Read full article:*\n"
		message_section_one += summary[i]['article_url']+"\n\n"

		final_message = message_separator + message_section_one + message_section_two		
		file.write(final_message)

	file.close()

def generate_abhivyakti_whatsapp_message(summary):
	total_articles_count = len(summary)

	message_separator = "********************* New Message Starts Here *********************\n\n"

	message_section_two = "-----------------------------------------------------------\n 📱 _Join Abhivyakti's English Whatsapp Channel:_\nhttps://chat.whatsapp.com/IYdOYT4MuCtDNhkgHoVKn0\n\n"
	message_section_two += "📱 _अभिव्यक्तीचे मराठी/हिंदी व्हाट्सएप चॅनेलला जॉईन करा:_\nhttps://chat.whatsapp.com/Dvrwcdpw0TdDYMsRciyufS\n\n"
	message_section_two += "📱 _Like Janata Weekly Facebook page:_\nhttps://www.faceboook.com/janataweekly\n\n"

	message_section_one = ""

	file = open("EnglishWhatsappMessagesWithAbhivyaktiFooter.txt","w",encoding="UTF-8")
	for i in range(1,total_articles_count):
		message_section_one = "⭕ *"+summary[i]['article_title'].strip()+"*\n\n"
		message_section_one += "✒️ "+summary[i]['article_author']+"\n\n_"+summary[i]['article_excerpt'].strip()+"_\n\n*Read full article:*\n"
		message_section_one += summary[i]['article_url']+"\n\n"

		final_message = message_separator + message_section_one + message_section_two
		file.write(final_message)

	file.close()