import textract
filename="Gandhi’s Idea of Cleanliness and Swachh Bharat Abhiyan_Sandeep Pandey_ed.doc"
with open('temp.txt','wb') as temp_text_file:
    temp_text_file.write(textract.process(filename))
title=''
body=''
title_index=0
with open('temp.txt','r') as temp_text_file:
    data=temp_text_file.readlines()
    for line in data:
        if line!='\n':
            title_index=data.index(line)
            break
    title=data[title_index]
    raw_para_list=''.join(data[title_index+1:]).split('\n\n')
    processed_para_list=[]
    for para in raw_para_list:
        processed_para_list.append(para.replace('\n',' '))
    body='\n\n'.join(processed_para_list)
print(title)
print(body)


