import json
import random
import os
import re

# file_path = "./COIG-PC/data/00043-000-000-machine-reading-comprehension.jsonl"
# file_path = "./COIG-PC/data/00222-002-000-info_extraction.jsonl"
folder_path = "./COIG-PC/data/"
# 读取 JSON 文件
def select_reading_comprehension(file_name):

    with open(folder_path + file_name, encoding='utf-8') as file:
        # 解析第一行 JSON 数据
        first_line = file.readline()
        data = json.loads(first_line)
        task_type = data["task_type"]
        major = task_type["major"]
        minor = task_type["minor"]
        if type(major) == str and major == "摘要":
            return "zhaiyao"
        if type(major) == list and major == ["信息抽取", "语义分析"]:
            return "xinxi_yuyi"
        if type(major) == str and major == "自然语言推理":
            return "ziranyuyan"
        if type(major) == list and major == ["摘要", "翻译", "常识"]:
            return "zhaiyao_fanyi_changshi"
        if type(major) == list and major == ["自然语言推理", "常识", "翻译"]:
            return "ziran_changshi_fanyi"
        # return data

# for root, dirs, files in os.walk(folder_path):
#     for file_name in files:
#         # 获取文件的完整路径
#         source_file = os.path.join(root, file_name)
        
#         num = select_reading_comprehension(file_name)
#         if num:
#             destination_file = './data/' + num + '/' +file_name
#             # 打开源文件和目标文件
#             with open(source_file, 'rb') as src_file, open(destination_file, 'wb') as dest_file:
#             # 从源文件读取内容，并将其写入目标文件
#                 dest_file.write(src_file.read())
#             with open(num + '.txt', 'a', encoding='utf-8') as f:
#                 f.write(file_name + '\n')
#                 print(file_name)
        # else:
            # with open('read.txt', 'a', encoding='utf-8') as f:
            #     f.write(str({file_name: num}))
            #     f.write('\n')
            #     print(file_name + ':' + str(num))

files_name = "selected.txt"
def find_json_list(file_name):
    json_list = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            # 使用正则表达式匹配第一个单引号之间的字符串
            match = re.search(r"'(.*?)'", line)
            # 如果匹配成功
            if match:
                # 提取匹配到的字符串
                result = match.group(1)
                json_list.append(result)
    return json_list

def seleted_copy():

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 获取文件的完整路径
            if file_name in find_json_list(files_name):
                source_file = os.path.join(root, file_name)
                destination_file = './data/reading_comprehension/' + file_name
                # 打开源文件和目标文件
                with open(source_file, 'rb') as src_file, open(destination_file, 'wb') as dest_file:
                    # 从源文件读取内容，并将其写入目标文件
                    dest_file.write(src_file.read())
                with open('reading_comprehension.txt', 'a', encoding='utf-8') as f:
                    f.write(file_name + '\n')
                    print(file_name)
    print("---------------------------筛选完成-----------------------------")
rc_folder_path = './data/yuedulijie/'

def file_line():
    for root, dirs, files in os.walk(rc_folder_path):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            with open(source_file, 'r', encoding='utf-8') as file, open('read_com.txt', 'a', encoding='utf-8') as f:
                first_line = file.readline()
                f.write(str({file_name: first_line}))
                f.write('\n')
            print(file_name)
# seleted_copy()

num_lines = 400
input_path = './data/reading_comprehension/'
output_path = "./data/selected/"

def extract():
    json_files = []
    # 遍历每个JSON文件
    for root, dirs, files in os.walk(input_path):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            json_files.append(source_file)
    for file_path in json_files:
        # 打开JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 加载JSON数据
            lines = file.readlines()

            # 移除行尾的换行符
            lines = [line.strip() for line in lines]
        
            # 随机抽取指定行数的数据
            if len(lines) >= num_lines:
                sampled_lines = random.sample(lines, num_lines)
            else:
                sampled_lines = lines
        
        # 保存抽样的数据到新文件
        print(file_path.split("/")[-1])
        output_file_path = output_path + "/" + file_path.split("/")[-1]
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            for line in sampled_lines:
                output_file.write(line)
                output_file.write('\n')
    print("---------------------------抽取完成-----------------------------")

# file_line()
seleted_copy()
extract()

input_data = './data/00452-000-000-news_topic_classification.jsonl'
output_data1 = './data/00452-000-003-news_topic_classification.jsonl'
output_data2 = './data/00452-000-004-news_topic_classification.jsonl'

def split_json_file(input_file, output_file1, output_file2):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    num_lines = len(lines)
    half_lines = num_lines // 2

    with open(output_file1, 'w', encoding='utf-8') as f1:
        f1.writelines(lines[:half_lines])

    with open(output_file2, 'w', encoding='utf-8') as f2:
        f2.writelines(lines[half_lines:])

split_json_file(input_data, output_data1, output_data2)
