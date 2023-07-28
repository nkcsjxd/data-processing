from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time,requests
import cv2
import numpy as np
from selenium.webdriver.common.by import By

#创建浏览器
driver = webdriver.Chrome()

#输入网址，打开该网站
driver.get('http://dun.163.com/trial/sense')

#点击网页

driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/ul/li[2]').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/span').click()
time.sleep(1)

k = 1
while True:
    #获取到两张图片链接
    bg_img_scr = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/img[1]').get_attribute('src')
    front_img_src = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/img[2]').get_attribute('src')

    #把图片下载到本地
    with open('./bg.jpg',mode='wb') as f:
        f.write(requests.get(bg_img_scr).content)
        f.close()
    with open('./front.jpg',mode='wb') as f:
        f.write(requests.get(front_img_src).content)
        f.close()

    #读取图片
    bg = cv2.imread('./bg.jpg')
    front = cv2.imread('./front.jpg')

    #灰度处理
    bg = cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
    front = cv2.cvtColor(front,cv2.COLOR_BGR2GRAY)

    #去掉滑块黑色部分
    front = front[front.any(1)]#0表示黑色，1表示高亮部分

    #匹配->cv图像匹配算法
    result = cv2.matchTemplate(bg, front, cv2.TM_CCOEFF_NORMED)#match匹配,Template模板;精度高，速度慢的方法
    index_max = np.argmax(result)#返回的是一维的位置，最大值索引

    #反着推最大值的二维位置，和opencv是相反的
    x, y = np.unravel_index(index_max, result.shape)
    print ("二维中坐标的位置：",x, y)
    print ("正在进行第%s次滑动验证"%k)
    drop = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]')    
    ActionChains(driver).drag_and_drop_by_offset(drop, xoffset=y, yoffset=0).perform()
    time.sleep(1)
    
    #验证成功后获取“验证成功”，直到找到“验证成功”才跳出while True循环
    success = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[1]/div[2]/span[2]').text
    if success == '验证成功':            
        break
    else:
        print ('第%s次验证失败...'%k,'\n')
    k = k + 1
print ('已经通过验证码!!!') 
