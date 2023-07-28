import time
from bs4 import BeautifulSoup
from selenium import webdriver
import cv2 as cv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import random
from verify_code import Verifycode

# 设置 Chrome 无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# def getpagelist():
#     lst = []
#     driverg = webdriver.Chrome()
#     for webpage in range(1, 6):
#         time.sleep(1)
#         url_lst = f"https://ac.nowcoder.com/acm/problem/list?page={webpage}"
#         driverg.get(url_lst)
#         fapage = driverg.find_element_by_class_name('no-border')
#         # print('找到父网页')
#         sopage = fapage.find_elements_by_css_selector("tr")
#         # print('找到子网页')
#         for page in sopage:
#             lst.append(page.get_attribute('data-problemid'))
#         time.sleep(5)
#         # print('网页{}成功爬取'.format(webpage))
#     lst = [x for x in lst if x is not None]
#     driverg.quit()
#     with open("C:/Users/Administrator/Desktop/shixun/pagelist.txt",'w') as file:
#         for item in lst:
#             file.write("%s\n" % item)



#
# if not os.path.exists("C:/Users/Administrator/Desktop/shixun/pagelist.txt"):
#     getpagelist()
#
# f=open("C:/Users/Administrator/Desktop/shixun/pagelist.txt",encoding='gbk')
# for line in f:

# problemId = int(line)

username = '13804204446'
password = '*math13804204446'
sleep_time = random.random() * 0.5 + 1
save_path = 'D:\\Workspace\\PycharmProjects\\Code-pre\\crawler\\bmm_crawler\\code\\nowcoder_spider\\'

def divTextProcess(div):
    strBuffer = div.get_text()
    strBuffer = strBuffer.replace("{", " $").replace("}", "$ ")
    strBuffer = strBuffer.replace("  ", "")
    strBuffer = strBuffer.replace("\n\n\n", "\n")
    strBuffer = strBuffer.replace("\xa0", "")
    strBuffer = strBuffer.strip()
    return strBuffer

def page_update(driver):

    # 焦点回到最新打开的页面
    init = driver.window_handles
    driver.switch_to.window(init[-1])

def login():

    # 切换到密码登录
    driver.find_elements(By.CLASS_NAME, "tab-item")[1].click()

    # 输入账号密码
    lst=driver.find_elements(By.CLASS_NAME, 'el-input__inner')
    lst[0].send_keys(username)
    time.sleep(sleep_time)
    lst[1].send_keys(password)

    # 下次自动登录
    driver.find_elements(By.CLASS_NAME, "el-checkbox__inner")[1].click()
    time.sleep(sleep_time)

    # 登录
    login=driver.find_elements(By.CLASS_NAME, "el-button")[0]
    login.click()

    # 30秒的时间 手动验证 反爬程序还需编写
    time.sleep(sleep_time * 10)

    # 使用验证脚本
    # if verifycode.is_slide():
    #     verifycode.slide_code()
    #     if verifycode.is_success():
    #         print('slide success')
    #     else:
    #         print('slide failure')
    # elif verifycode.is_pick():
    #     cjy,result = verifycode.pick_code()
    #     if verifycode.is_success():
    #         print('pick click success')
    #     else:
    #         print('pick click failure')
    #         if result['err_no'] == 0:
    #             r = cjy.ReportError(result['pic_id'])
    #             print(r)

    driver.close()
    driver.switch_to.window(window)   #关掉第一题，切回主界面
    time.sleep(sleep_time)

def problem_page():

    # 找到题目列表对应表格
    table = driver.find_element(By.CLASS_NAME, 'no-border')

    # 找到题目序号标签
    sopage = table.find_elements(By.CSS_SELECTOR, "tr")

    # 第一个tr不包含题目，跳过
    problemIdlist=[]
    for page in sopage:
        problemIdlist.append(page.get_attribute('data-problemid'))
    return problemIdlist

def problem(driver, problemId):

    # 获取页面信息
    soup = BeautifulSoup(driver.page_source,'lxml')
    data_dict = {}
    # 找到主体内容
    # mainContent = soup.find_all(name="div", attrs={"class" :"terminal-topic"})[0]
    div_list = soup.find_all(name="div", attrs={"class" :"terminal-topic"})
    if len(div_list) > 0:
        mainContent = div_list[0]
        # 处理mainContent
    else:
        print("未找到目标元素")
        return data_dict
    for each in mainContent.find_all('mrow'):
        each.decompose()
    for each in mainContent.find_all(name="span", attrs={"class" :"katex-html"}):
        each.decompose()
    # 更换换行符
    for each in mainContent.find_all('br'):
        each.replace_with("\n\n")

        # Limit
        # 找到题目标题、时间、和内存限制
        div = mainContent.find_all(name="div", attrs={"class": "subject-item-wrap"})[0].find_all("span")
        # Title
        # data_dict['Title'] = f"牛客网 NC{problemId} " + '<' + soup.title.contents[0] + '>'
        data_dict['Title'] = soup.title.contents[0]
        # Time Limit
        # data_dict['Time Limit'] = div[1].contents[0].split('：')[1]
        # Memory Limit
        # data_dict['Memory Limit'] = div[2].contents[0].split('：')[1]

    # 处理题目描述
    div = mainContent.find_all(name="div", attrs={"class": "subject-question"})[0]
    data_dict['Problem Description'] = divTextProcess(div)

    div = mainContent.find_all(name="pre")[0]
    data_dict['Input'] = divTextProcess(div)

    div = mainContent.find_all(name="pre")[1]
    data_dict['Output'] = divTextProcess(div)

    try:
        # Input
        div = mainContent.find_all(name="div", attrs={"class":"question-oi-cont"})[0]
        data_dict['Sample Input'] = div.get_text()
        # Onput
        div = mainContent.find_all(name="div", attrs={"class":"question-oi-cont"})[1]
        data_dict['Sample Onput'] = div.get_text()
    except IndexError:
        print("没有输入输出示例")

    # 若有备注
    if len(mainContent.find_all(name="pre")) >= 5:
        div = mainContent.find_all(name="pre")[-1]
        data_dict['Note'] = divTextProcess(div)
  
    return data_dict

def analysis():

    driver = webdriver.Chrome()
    url = f"https://ac.nowcoder.com/acm/problem/blogs/{problemId}"
    driver.get(url)
    time.sleep(sleep_time)

    # 判断是否折叠
    unfolds = driver.find_elements(By.CLASS_NAME, "more-unfold")
    counts = len(unfolds)
    analysis_list = []
    if unfolds:
        for i in range(counts):
            try:
                unfold = driver.find_elements(By.CLASS_NAME, "more-unfold")[i]
                unfold.click()
                time.sleep(sleep_time)
                try:
                    parent_div = unfold.find_element(By.XPATH, "./parent::div/parent::div")
                    div_element = parent_div.find_element(By.XPATH, ".//div[contains(@class, 'nc-post-content')]")
                    if div_element.text.strip() == '':
                        continue
                    codes = div_element.find_elements(By.CLASS_NAME, "prettyprint")
                    codetext = ''
                    for code in codes:
                        codetext += code.text
                    # print(code_list)
                    # 获取原始 HTML 内容
                    html_content = div_element.get_attribute('innerHTML')

                    # 使用 BeautifulSoup 解析 HTML
                    soup = BeautifulSoup(html_content, "html.parser")

                    # 查找所有的 <pre> 元素
                    pre_blocks = soup.find_all("pre")

                    # 删除所有的 <pre> 块
                    for pre in pre_blocks:
                        pre.decompose()
                    content = soup.get_text("\n")
                    # print(content)
                    dict = {'code': codetext, 'code_content': content}
                    analysis_list.append(dict)
                except NoSuchElementException:
                    print('{}号问题的题解没有示例代码'.format(problemId))
            except (ElementNotInteractableException, ElementClickInterceptedException):
                print('文字太短舍弃')
    else:
        print('{}号问题没找到题解'.format(problemId))
    driver.quit()
    time.sleep(sleep_time)
    return analysis_list

# 执行程序
driver = webdriver.Chrome()
url = "https://ac.nowcoder.com/acm/problem/list?page=2"
# 进入题目总界面不需要登录
driver.get(url)
time.sleep(sleep_time)
# 题目主界面句柄
window = driver.current_window_handle   
# 准备登录
driver.find_elements(By.PARTIAL_LINK_TEXT, 'NC')[0].click()
# 更新页面焦点
page_update(driver)
# 读取题目需要手动登录，有反爬机制
login()

for i in range(2, 216):
    # 获取问题ID列表
    problemIdlist = problem_page()
    # 题目主界面句柄
    window = driver.current_window_handle
    # 问题链接列表
    problemlist=driver.find_elements(By.PARTIAL_LINK_TEXT, 'NC')
    pnumber=len(problemlist)

    for pnum in range(pnumber):
        # 进入问题页面
        driver.execute_script("arguments[0].click();", problemlist[pnum])
        page_update(driver)
        time.sleep(sleep_time)
        # 获取问题题号problemId
        try: 
            problemId=int(problemIdlist[pnum+1])
        except IndexError:
            continue
        # 获得问题描述
        data_dict = problem(driver, problemId)
        #问题描述部分获取完毕，获取解析
        code_dicts = analysis()
        if code_dicts:
            for code_dict in code_dicts:
                data_dict.update(code_dict)
                # 写入json文件
                json_path = save_path + f"problem_page{i}.json"
                with open(json_path, 'a',encoding='utf-8',errors='ignore') as f:
                    f.write(str(data_dict) + '\n')
                    f.close()
            print('输出文件')
        # 关闭题目页面，切换到主页面
        driver.close()
        driver.switch_to.window(window)
        time.sleep(sleep_time)
        '''测试使用每页读取一个题目，正式使用请注释掉break'''
        # break
    '''最后一页可能会有问题，还没有测试'''
    if i == 215: pass
    else:
        # 下一页
        element = driver.find_elements(By.CLASS_NAME, 'txt-pager')[2]
        driver.execute_script("arguments[0].click();", element)
        




