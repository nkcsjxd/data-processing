# -*coding:utf-8*-
import time
from DownloadKit import DownloadKit
from DrissionPage import SessionPage, SessionOptions
import re
import os
from tqdm import tqdm
if not os.path.exists('压缩包'):
    os.mkdir('压缩包')
session = SessionPage()
do=DownloadKit(session=session,file_exists='skip',roads=10)
url = 'https://www.shijuan1.com/'
header = {
    'Cookie': 'Hm_lvt_9400c877dfe1cf77b070ccf1be7b66af=1689328475; __gads=ID=1a7956109b8b7c14-22ed119aa7e200c8:T=1689328474:RT=1689328474:S=ALNI_MZ9J67oaMTss6eqFO9mKhZ-jmbbng; __gpi=UID=00000cbf0e0c3460:T=1689328474:RT=1689328474:S=ALNI_Ma6R0LX-bJGtPpdREHR0FagEmdzrw; Hm_lpvt_9400c877dfe1cf77b070ccf1be7b66af=1689328666',
    'Host': 'www.shijuan1.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
session.get(url, headers=header)

uls = session.s_eles('xpath://div[@class="linkbox"]/ul')
for ul in uls:
    lis = ul.s_eles('xpath:./li')
    title_all = lis[0].s_ele('xpath:/a').text
    if title_all in ['语文试卷', '政治试卷', '历史试卷']:
        if not os.path.exists(f'压缩包/{title_all}'):
            os.mkdir(f'压缩包/{title_all}')
        for li in lis[1:]:
            href = li.s_ele('xpath:/a').attr('href')
            title=li.s_ele('xpath:/a').text
            if title not in ['一年级','二年级','三年级','四年级']:
                if not os.path.exists(f'压缩包/{title_all}/{title}'):
                    os.mkdir(f'压缩包/{title_all}/{title}')
                session.get(href,headers=header)
                page_num=re.findall('共(.*?)页',session.s_ele('xpath://span[@class="pageinfo"]').text)[0]
                if int(page_num)>1:
                    href_two_lst=session.s_eles('xpath://ul[@class="pagelist"]/li/a')[0].attr('href').rsplit('_',1)#二级页面
                    for i in tqdm(range(1,int(page_num)+1)):
                        href_two=href_two_lst[0]+'_'+str(i)+href_two_lst[1][1:]
                        # print(href_two)
                        session_one_session=session.session
                        session_two=SessionPage(session_or_options=session_one_session)
                        header_two={
                            'Cookie': 'Hm_lvt_9400c877dfe1cf77b070ccf1be7b66af=1689304903,1689330531; Hm_lpvt_9400c877dfe1cf77b070ccf1be7b66af=1689331067',
                            'Host': 'www.shijuan1.com',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
                        }
                        session_two.get(href_two,headers=header_two)
                        time.sleep(1)
                        trs=session_two.s_eles('xpath://ul[@class="c1"]//tr')
                        for tr in trs[1:]:
                            title_href=tr.s_ele('xpath://a').text
                            href_href=tr.s_ele('xpath://a').attr('href')
                            if '解析' in title_href or '答案' in title_href:#三级页面
                                header_three={
                                    'Cookie': 'Hm_lvt_9400c877dfe1cf77b070ccf1be7b66af=1689304903,1689330531; Hm_lpvt_9400c877dfe1cf77b070ccf1be7b66af=1689331592',
                                    'Host': 'www.shijuan1.com',
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
                                }
                                session_two_session=session_two.session
                                session_three=SessionPage(session_or_options=session_two_session)
                                session_three.get(href_href,headers=header_three)

                                download_href=session_three.s_ele('xpath://ul[@class="downurllist"]//a').attr('href')
                                do.add(download_href,rename=title_href,goal_path=f'压缩包/{title_all}/{title}')
                                # do.show()
                        print(f'{title}{title_all}第{i}页下载完成')
                else:
                    trs = session.s_eles('xpath://ul[@class="c1"]//tr')
                    for tr in trs[1:]:
                        title_href = tr.s_ele('xpath://a').text
                        href_href = tr.s_ele('xpath://a').attr('href')
                        if '解析' in title_href or '答案' in title_href:  # 三级页面
                            header_three = {
                                'Cookie': 'Hm_lvt_9400c877dfe1cf77b070ccf1be7b66af=1689304903,1689330531; Hm_lpvt_9400c877dfe1cf77b070ccf1be7b66af=1689331592',
                                'Host': 'www.shijuan1.com',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
                            }
                            session_two_session = session.session
                            session_three = SessionPage(session_or_options=session_two_session)
                            session_three.get(href_href, headers=header_three)

                            download_href = session_three.s_ele('xpath://ul[@class="downurllist"]//a').attr('href')
                            do.add(download_href, rename=title_href, goal_path=f'压缩包/{title_all}/{title}')
                            # do.show()
                    print(f'{title}{title_all}第1页下载完成')
    else:
        continue

if __name__ == '__main__':
    pass
