import docx

def get_summary_data(summaryfile):
    doc = docx.Document(summaryfile)
    file_data=[]
    summary_data=[]
    for para in doc.paragraphs:
        if para.text == '':
            continue
        file_data.append(para.text)
    for i in range(1, len(file_data),3):
        article_number, article_title = file_data[i].split('.')
        article_author_pre = file_data[i+1].split(' ')
        if article_author_pre[0] == 'by':
            article_author_pre.remove('by')
        article_author = ' '.join(article_author_pre).strip(' ')
        article_exerpt = file_data[i+2] 
        summary_data.append(
                            {
                                'article_number' : article_number,
                                'article_title' : article_title,
                                'article_author' : article_author,
                                'article_exerpt' : article_exerpt
                            }
                        )      

    return summary_data



def get_article_data(articlefile):
    article_number = articlefile.split('/')[-1].split('-')[0]
    doc=docx.Document(articlefile)
    article_title = doc.paragraphs[0].text
    file_data=[]
    for para in doc.paragraphs:
        print(len(para.runs))
        for run in para.runs:
            print(run.text)
        file_data.append(para.text)
    article_body = '\n'.join(file_data[1:])
    article = {
                    'article_number' : article_number,
                    'article_title' : article_title,
                    'article_body' : article_body
                }
    return article

'''
summaryfile='C:/Users/akshay.raut/Downloads/Summary.docx'  
articlefile='C:/Users/akshay.raut/Desktop/JAP/JAP/gDocParser/13-How Racism is an Essential Tool for Maintaining the Capitalist Order_Richard D. Wolff.docx'
a=get_article_data(articlefile)'''

