import requests
from bs4 import BeautifulSoup
import time
import random
import os
from requests.exceptions import InvalidSchema

# 发起HTTP请求，获取网页的HTML内容
# url = 'http://www.a-hospital.com/w/中医图书下载索引-Z'  # 替换为你要爬取的网站URL

url = "http://www.37med.com/soft/yysj/chyx/"
save_path = './txt/chyx/'

def download_txt_file(url, text, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if content_type:
            file_extension = content_type.split('/')[-1]

            # 组合保存路径和文件名
            file_path = os.path.join(save_path, f"{text}.{file_extension}")

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"文件下载成功，保存为 {file_path}")

    else:
        print("文件下载失败")

def link_element(selector, url):
    link_text = []
    link_url = []
    # 查找单元格中的链接
    # if soup_response(url) != 0:
    div_elements = soup_response(url).select(selector)  # 找到指定的div元素
    for div_element in div_elements:
        link_element = div_element.find('a')
        if link_element:
            link_text.append(link_element.text.strip())  # 链接的文本内容
            link_url.append(link_element['href'])  # 链接的URL
            print(f"链接文本：{link_element.text.strip()}")
            print(f"链接URL：{link_element['href']}")
        else:
            print("未找到")
    print("操作结束")
    return link_text, link_url

def soup_response(url):
    # 设置随机延时
    delay = random.uniform(2, 5)  # 随机生成 0.5 到 2 秒之间的延时
    time.sleep(delay)
    try:
        response = requests.get(url)
        response.encoding = 'gbk'
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        else:
            print("请求失败")
    except InvalidSchema:
        # 在这里处理无效的URL错误
        print("Invalid URL provided. Skipping request.")
        return 0
    
        
    
    

# 医学电子书
# selector = "body div#content div#bodyContent ul li"
# link_texts, link_urls = link_element(selector, url)
# for link_url in link_urls:
#     url = 'http://www.a-hospital.com' + link_url
#     selector = "body > div#content > div#bodyContent > div.fullMedia > p > span.dangerousLink"
#     new_link_texts, new_link_urls = link_element(selector, url)
#     for i in range(0, len(new_link_urls)):
#         download_txt_file(new_link_urls[i], new_link_texts[i], save_path)

# selector = "body > div.main > div.col-left > div.box.boxsbg > dl.down_list.sysnews > dt > h5"
# link_texts, link_urls = link_element(selector, url)
# selector = "body > div.main > div.col-left > div.box.boxsbg > div.contents > div.down_address.divl.wrap > ul.l.xz_a.wrap.blue > li"
# for link_url in link_urls:
#     new_link_texts, new_link_urls = link_element(selector, link_url)
#     new_selector = "body"
#     for link_url in new_link_urls:
#         div_elements = soup_response(link_url).select(new_selector)
#         for div_element in div_elements:
#             link_elements = div_element.find('a')
#             dl_text = new_link_texts[new_link_urls.index(link_url)] # 链接的文本内容
#             # dl_text = link_elements.text.strip()
#             dl_link = "http://www.37med.com/index.php" + link_elements['href']  # 链接的URL
#             print(f"链接文本：{dl_text}")
#             print(f"链接URL：{dl_link}")
#             download_txt_file(dl_link, dl_text, save_path)

folder_path = "./txt/zhongyi/"

# # 遍历文件夹
# for file in os.listdir(folder_path):
#     # 获取文件的绝对路径
#     file_path = os.path.join(folder_path, file)
#     # 判断是否是文件
#     if os.path.isfile(file_path):
#         # 处理文件
#         new_file_path = file_path[:len(file_path)-21]  # 打印文件路径或进行其他操作
#         with open(file_path, 'wb') as file:
#                 file.write(chunk)

import os
for filename in os.listdir(folder_path):   #‘logo/’是文件夹路径，你也可以替换其他
	newname = filename.replace('.plain; charset=utf-8', '')  #把jpg替换成png
	os.rename(folder_path+filename, folder_path+newname)  
