import docx

def _is_article_line(line):
    """Returns True if line looks like '1. Title...' — a numbered article entry."""
    parts = line.split('.', 1)
    return len(parts) == 2 and parts[0].strip().isdigit()

def get_summary_data(summaryfile):
    doc = docx.Document(summaryfile)
    file_data = []
    summary_data = []
    for para in doc.paragraphs:
        if para.text.strip() in ('', '\n', ' '):
            continue
        file_data.append(para.text)

    i = 0
    while i < len(file_data):
        if not _is_article_line(file_data[i]):
            i += 1
            continue
        if i + 2 >= len(file_data):
            break
        parts = file_data[i].split('.', 1)
        article_number = parts[0].strip()
        article_title = parts[1].strip()
        article_author_pre = file_data[i+1].split(' ')
        if article_author_pre[0].lower() == 'by':
            article_author_pre = article_author_pre[1:]
        article_author = ' '.join(article_author_pre).strip()
        article_excerpt = file_data[i+2]

        summary_data.append(
                            {
                                'article_number' : article_number,
                                'article_title' : article_title,
                                'article_author' : article_author,
                                'article_excerpt' : article_excerpt
                            }
                        )
        i += 3

    return summary_data

def get_general_summary(summaryfile):
    summary_data = get_summary_data(summaryfile)
    general_summary = {
                            'titles' :  [summary_data_dict['article_title'] for summary_data_dict in summary_data],
                            'authors' : [summary_data_dict['article_author'] for summary_data_dict in summary_data],
                            'excerpts' : [summary_data_dict['article_excerpt'] for summary_data_dict in summary_data]
                      }

    return general_summary

