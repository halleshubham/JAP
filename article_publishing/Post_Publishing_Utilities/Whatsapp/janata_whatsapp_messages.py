import datetime

def getSymbols(i):
	symbols = '0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟'
	x=str(i)
	if(len(x)==1):
		return((symbols[3*(int(i))])+(symbols[3*(int(i))+2]))
	else:
		i=str(i)
		a=getSymbols(i[0])
		b=getSymbols(i[1])
		return(a+b)


def generate_janata_whatsapp_messages(summary, publish_date):

	message_section_one = '📮 *Janata Weekly*\n'
	message_section_one += 'India\'s oldest socialist magazine!\n\n'
	message_section_three = 'Vol.75, No. '+ str(datetime.date.today().isocalendar()[1] - 4) +' | '+publish_date.strftime('%d %B, %Y')+' Issue\n\n'
	message_section_three += 'Editor: Dr.G.G. Parikh \nAssociate Editor: Neeraj Jain \nManaging Editor: Guddi\n\n'

	message_section_five = "\n➖➖➖➖➖➖➖➖➖➖➖\n\n📋 *About Janata Weekly :*\nJanata Weekly is an *independent socialist journal*. It has raised its challenging voice of principled dissent against all conduct and practice that is detrimental to the cherished values of nationalism, democracy, secularism and socialism, while upholding the integrity and the ethical norms of healthy journalism. It has the enviable reputation of being the oldest continuously published socialist journal in India."
	message_section_five += "\n\n📢 Oldest socialist weekly of India, is now also on facebook!\n"
	message_section_five +='👍 https://facebook.com/JanataWeekly \n\n'
	message_section_five += "📋 *Subscribe to Hard Copy*\n\nAnnual: Rs. 260 /-\nThree Years : Rs. 750 /-\n\n📲 Guddi: 07738082170\n➖➖➖➖➖➖➖➖➖➖➖\n\n"
	message_section_five += "📬 *To recieve Janata directly to your mailbox*\n\nFill this form: https://janataweekly.org/subscribe/\n\n📬 *Join for WhatsApp version* \n"
	message_section_five += "\n*🔴 Group 1*: https://chat.whatsapp.com/GFy7sR6uV9bD9gt5dlhE7D\n\n*🔴 Group 2*: https://chat.whatsapp.com/Gvp7JM00VvZKMeh6ld302v"

	total_articles_count = len(summary)

	total_parts = 7
	equally_divided_articles_count = int (total_articles_count/ total_parts)
	remaining_extra_articles_count = total_articles_count % total_parts
	upperLimit = equally_divided_articles_count
	lowerLimit = 0

	for part in range(1, total_parts+1):			
		message_section_two =  '*Part '+str(part)+' of '+ str(total_parts)+'*\n'

		if (part < remaining_extra_articles_count):
			upperLimit += 1
		
		message_section_four = ''
		for i in range(lowerLimit, upperLimit):
			message_section_four += getSymbols((1+int(i)))+" *"
			message_section_four += summary[i]['article_title'].strip()+"*\n\n✒️ _"+summary[i]['article_author']+"_\n\n"

			if (i != (upperLimit-1)):
				message_section_four += summary[i]['article_link'] +"\n-----------------------------------------------------------\n\n"
			else:
				message_section_four += summary[i]['article_link']

		lowerLimit = upperLimit
		upperLimit += equally_divided_articles_count

		final_message = message_section_one + message_section_two + message_section_three + message_section_four + message_section_five
		f1 = open("janata_whatsapp_message"+str(part)+".txt","w",encoding="UTF-8")
		f1.write(final_message)
		f1.close()
		



