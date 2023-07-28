import chm
import os

def chm_to_txt(file_path):
    chm_file = chm.CHMFile(file_path)
    # 获取所有内容页
    content_pages = chm_file.pages()
    
    extracted_text = ""
    
    # 提取每个内容页的文本
    for page in content_pages:
        extracted_text += page.extract_text()
    
    return extracted_text

chm_path = './chm/'
txt_path = './txt/'

for file_name in os.listdir(chm_path):
        file_path = os.path.join(chm_path, file_name)
        if os.path.isfile(file_path):
            print(file_name)
            output_file = txt_path + file_name + '.txt'
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(chm_to_txt(file_path))
