# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 11:40:52 2020

@author: Felix
"""

import requests
from bs4 import BeautifulSoup

keyword = input('請輸入要取得免費課程的名稱，輸入完後按下Enter')

print(f"取得免費的{keyword}課程")

baseUrl = f'https://ke.qq.com/course/list/{keyword}?price_min=0&price_max=0'
response = requests.get(baseUrl)
if response.status_code == 200:
    html = response.text
    sp = BeautifulSoup(html,"lxml")

    #取得最大頁數
    maxPage = sp.find_all("a", class_="page-btn")[3].text
    print("共有 {0} 頁".format(maxPage))

    courseList = []
    for i in range(int(maxPage)):
        nowpage = i+1
        print("目前頁數",nowpage)
        
        url = f'{baseUrl}&page={nowpage}'
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            sp = BeautifulSoup(html,"lxml")
        
            #取得所有課程
            courseliList = sp.find_all("li", class_="js-course-card-item")
            for item in courseliList:
                img = item.img.get('src')
                if ('https' not in img):
                    img = 'https:'+img
                # print('img=',img)
                title = item.h4.text.strip()
                print('課程名稱：',title)
                href = item.h4.a.get('href')
                # print('href=',href)                
                peoplestr = item.find('span',class_='item-user').text.strip().replace('人最近报名','')
                if ('万' in peoplestr):
                    peoplestr = peoplestr.replace('万','0000')
                people = int(peoplestr)
                # print('people=',people)
                courseList.append({
                    'img':img,
                    'title':title,
                    'href':href,
                    'people':people
                    })
                
    #依報名人數排序
    courseSort = sorted(courseList, key=lambda k: k['people'], reverse=True)
    
    fileTitle = f'騰訊課堂免費的{keyword}課程'
    
    #組 Html 檔案內容
    html = '<!DOCTYPE html>'
    html += '<html xmlns=\"http://www.w3.org/1999/xhtml\">'
    html += '<head>'
    html += '<meta charset=\"utf-8\" />'
    html += f'<title>{fileTitle}</title>'
    html += '</head>'
    html += '<body>'
    html += '<table style=\"width: 60%; margin: auto; border:3px #cccccc solid;\" border=\"1\">'
    html += '<tr><th>No</th><th>圖片</th><th>課程名稱</th><th>報名人數</th><th>狀態</th></tr>'
    
    no=0
    for course in courseSort:
        no+=1
        href = course['href'] 
        html += f'<tr><td>{no}</td>'
        html += f'<td><a href=\"{href}\" target=\"_blank\"><img src=\"'+course['img']+'\"></a></td>'
        html += f'<td><a href=\"{href}\" target=\"_blank\">'+course['title']+'</a></td>'
        html += '<td>'+str(course['people'])+'</td><td></td></tr>'
    
    html += '</table>'
    html += '</body>'
    html += '</html>'
    
    #將結果輸出成 Html 檔
    fp = open(f'{fileTitle}.html','w',encoding='utf-8')
    fp.write(html)
    fp.close()
            