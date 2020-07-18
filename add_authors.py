from jap import get_summary_data,get_authors_list,add_authors

summaryfile='C:/Users/akshay.raut/Downloads/Summary.docx'
summary_data = get_summary_data(summaryfile)
authors_list = get_authors_list(summary_data)
add_authors(authors_list)
