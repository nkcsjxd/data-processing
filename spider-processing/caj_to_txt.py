import requests
import random
import time

# 设置要提交的文件路径
file_path = './caj./3D打印技术在泌尿外科的研究及应用进展.caj'

# 设置目标网站的URL
url = 'https://www.easeconvert.com/api/v1/fileCheck'

# # 发送POST请求，将文件作为表单数据提交
# files = {'file': open(file_path, 'rb')}
# # 设置随机延时
# delay = random.uniform(2, 5)  # 随机生成 0.5 到 2 秒之间的延时
# time.sleep(delay)
# response = requests.post(url, files=files)

# 上传文件
def upload_file(url, file_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        delay = random.uniform(2, 5)  # 随机生成 0.5 到 2 秒之间的延时
        time.sleep(delay)
        response = requests.post(url, files=files)
        return response.json()

# 下载处理后的文件
def download_file(url, save_path):
    delay = random.uniform(2, 5)  # 随机生成 0.5 到 2 秒之间的延时
    time.sleep(delay)
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

# 示例用法
upload_url = 'https://www.easeconvert.com/api/v1/upload'
convert_url = 'https://www.easeconvert.com/api/v1/convert'

# 上传文件
uploaded_file = upload_file(upload_url, file_path)
print(uploaded_file)

# 获取处理后的文件下载链接
file_id = uploaded_file['file_id']
download_url = f'{convert_url}/{file_id}/download'

# 下载处理后的文件
download_file(download_url, './txt/dl.zip')

# # 检查请求是否成功
# if response.status_code == 200:
#     print('文件提交成功！')
#     print(response.text)
# else:
#     print('文件提交失败。')
#     print(response.status_code)
#     print(response.text)