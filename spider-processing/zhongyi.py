# # 处理中医相关的txt文件，每篇放在一个raw_content里

# import os
# import re
# import json

# folder_path = './txt/zhongyi/'
# def txt_to_content(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         content = f.read()
#         # 删除文章前面无意义的内容
#         content = re.sub(r'[\s\S]*欢迎您的参与。\n\n', '', content)
#         # 删除所有\、英文、数字
#         content = re.sub(r'[\\a-zA-Z0-9 -.]', '', content)
#         content = re.sub(r'(\d)', '', content)
#         # 删除所有目录的哪那一行
#         content = re.sub(r'<目录>.*?\n', '', content)
#         # 删除所有单独的\n
#         content = re.sub(r'(?<!\n)\n(?!\n)', '', content)
#         # 删除所有<目录>、<篇名>、【介按】、属性：
#         content = re.sub(r'<篇名>|【介按】|属性：', '', content)
#         # 将\n\n\n变为\n\n
#         content = content.replace("\n\n\n", "\n\n")
#         return content

# def content_to_json(file_path):
#     data = {
#         'raw_content': txt_to_content(file_path)
#     }

#     # 检查目标文件夹是否存在，如果不存在则创建
#     output_dir = "./json/zhongyi/"
#     os.makedirs(output_dir, exist_ok=True)

#     output_file = os.path.join(output_dir, "data.json")

#     # 检查文件是否为空
#     if os.path.getsize(output_file) > 0:
#         # 文件不为空，从现有内容中读取JSON对象
#         with open(output_file, "r", encoding='utf-8') as json_file:
#             json_data = json.load(json_file)
#             # 将新内容追加到JSON列表中
#             json_data.append(data)
#             # json_str = json.dumps(json_data, ensure_ascii=False) + '\n' + json.dumps(data, ensure_ascii=False)
#     else:
#         # 文件为空，创建初始JSON结构
#         json_data = [data]
#         # json_str = json.dumps(data, ensure_ascii=False)

#     # 将txt文件内容对象写入json文件
#     with open(output_file, "w", encoding='utf-8') as json_file:
#         # json_file.write(json_str)
#         json.dump(json_data, json_file, ensure_ascii=False)

# for file_name in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file_name)
#         if os.path.isfile(file_path):
#             print(file_name)
#             content_to_json(file_path)

import os
import re
import json

# folder_path = './txt/zhongyi/'

# def txt_to_content(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         content = f.read()
#         content = re.sub(r'[\s\S]*欢迎您的参与。\n\n', '', content)
#         content = re.sub(r'[\\a-zA-Z0-9 -.]', '', content)
#         content = re.sub(r'(\d)', '', content)
#         content = re.sub(r'<目录>.*?\n', '', content)
#         content = re.sub(r'(?<!\n)\n(?!\n)', '', content)
#         content = re.sub(r'<篇名>|【介按】|属性：', '', content)
#         content = content.replace("\n\n\n", "\n\n")
#         print("文件读取完成")
#         return content

# def process_files(file):
    
#     content = txt_to_content(file)
#     data = {
#         'raw_content': content
#     }
#     print(file)
#     return data

# def content_to_json(output_file, json_data):
#     with open(output_file, "a", encoding='utf-8') as json_file:
#         json.dump(json_data, json_file, ensure_ascii=False)
#         json_file.write('\n')
        

# def process_folder(folder_path, output_file):
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
#     file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_name))]

#     for file in file_paths:
#         json_data = process_files(file)
#         content_to_json(output_file, json_data)

# output_file = "./json/zhongyi/data.json"
# process_folder(folder_path, output_file)


folder_path = './txt/zhongyi/'
output_file = "./json/zhongyi/data.json"

def txt_to_content(file_path):
    content = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk_size = 8192  # 设置缓冲区大小
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            content += data
    # 文本处理操作，根据您的需要进行修改
    content = re.sub(r'[\s\S]*欢迎您的参与。\n\n', '', content)
    content = re.sub(r'[\\a-zA-Z0-9 -.]', '', content)
    content = re.sub(r'(\d)', '', content)
    content = re.sub(r'<目录>.*?\n', '', content)
    content = re.sub(r'(?<!\n)\n(?!\n)', '', content)
    content = re.sub(r'<篇名>|【介按】|属性：|□', '', content)
    content = content.replace("\n\n\n", "\n\n")
    print("文本处理成功")
    return content

def process_files(file):
    content = txt_to_content(file)
    return {'raw_content': content}

def process_folder(folder_path, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "a", encoding='utf-8') as json_file:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                json_data = process_files(file_path)
                json.dump(json_data, json_file, ensure_ascii=False)
                json_file.write('\n')

process_folder(folder_path, output_file)

# # 读取JSON文件
# with open('./json/zhongyi/data.json', 'r', encoding='utf-8') as file:
#     # 解析JSON数据
#     data = json.load(file)

# # 将列表中的每个元素逐行写入到JSON文件
# with open('./json/zhongyi/datas.json', 'a', encoding='utf-8') as file:
#     for item in data:
#         # 创建一个包含当前元素的列表
#         # output_data = [item]
#         # 写入当前元素到JSON文件，并添加换行符
#         output_data = json.dumps(item, ensure_ascii=False)
#         file.write(output_data + '\n')
