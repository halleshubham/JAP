import docx
import json
import unicodedata


def get_summary_data(filepath):
    doc = docx.Document(filepath)
    summary_data=[]
    author=[]
    excerpt=[]
    title=[]
    for para in doc.paragraphs:
        
        if (para.text != '') and (para.text != ' '):
            if (len(author)== len(excerpt)==len(title)): 
                title1=para.text
                title1=title1.split('. ',1)
                title.append(unicodedata.normalize("NFKD",title1[1]))
                continue
            if (len(excerpt)==len(author)) and (len(excerpt)!=len(title)):
                author.append(unicodedata.normalize("NFKD",para.text))
                continue
            if (len(author)==len(title)) and (len(excerpt)!=len(author)):
                excerpt.append(unicodedata.normalize("NFKD",para.text))
                continue
        
    summary_data.append(
                        {
                            'titles' : title,
                            'authors' : author,
                            'excerpts' : excerpt
                        }
                    )      

    return summary_data





