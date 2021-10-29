import docx
import json
import unicodedata

def get_summary_data(filepath):
    doc = docx.Document(filepath)
    summary_data=[]
    author=[]
    excerpt=[]
    title=[]
    for para in doc.paragraphs[1:]:
        
        if (para.text != '') and (para.text != ' ') and (para.text != 'Print') and (para.text != ('Blog')):
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

    #n = len(title)
    #Newauthor=[None] * n
    #Newexcerpt=[None] * n
    #Newtitle=[None] * n
    #for i in range(0,n):
    #    Newauthor[i] =author[n-1-i]
    #    Newexcerpt[i] =excerpt[n-1-i]
    #    Newtitle[i] =title[n-1-i]

    summary_data.append(
                        {
                            'titles' : title,
                            'authors' : author,
                            'excerpts' : excerpt
                        }
                    )      

    return summary_data





