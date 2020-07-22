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
        li=file_data[i].split('.')
        article_number=li[0]
        article_title = '.'.join(li[1:])
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



