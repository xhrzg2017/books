#!/usr/bin/python
# encoding: utf-8


"""
@author: B站@电脑初哥
@contact: 1009019824@qq.com
@file: demo.py
@time: 2020/3/13 17:51
"""

import time
import os
import parsel
import requests
from fake_useragent import UserAgent

ua=UserAgent

print('B站@电脑初哥 研发 ')
print('站长别打我 ')
print('开始工作...')

'''网站首页分栏链接'''
def download_web(url):
        try:
            response = requests.get(url,headers=headers,timeout=5)
        except Exception as e:
            print(e)
        else:
            selector = parsel.Selector(response.text)
            #print(selector)
            urls = selector.css('#wrapper > div.nav > ul > li > a::attr(href)').getall()
            for url in urls[2:9]:
                #print(url)
                download_category('https://www.biquge.tw' + url)

'''小说简介链接'''
def download_category(url):
    print(url)
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        print(e)
    else:
        selector = parsel.Selector(response.text)
        # print(selector)
        urls = selector.css('#newscontent > div.l > ul > li> span.s2 > a::attr(href)').getall()
        for url in urls:
            # print(url)
            download_one_book('https://www.biquge.tw/' + url)


'''小说章节链接'''
def download_one_book(url):
    print(url)
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        print(e)
    else:
        selector = parsel.Selector(response.text)
        name = selector.css('#info > h1::text').get()
        url_s = selector.css('#list > dl > dd > a::attr(href)').getall()
        for url in url_s[12:22]:
            print('正在拷贝书名：' + name + '\000' + ' 中...')
            print('https://www.biquge.tw/' + url)
            download_one_chapter('https://www.biquge.tw/' + url, name)



'''保存小说'''
def download_one_chapter(url, name):
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        print(e)
    else:
        selector = parsel.Selector(response.text)

        title = selector.css('#wrapper > div.content_read > div.box_con > div.bookname > h1::text').get()
        print(title)
        content = selector.css('#content::text').getall()
        text = ""
        for i in content:
            text = text + i.strip() + '\n'
        path = '/books'
        if not os.path.exists(path):
            os.makedirs(path)
        # print(title, text)
        with open(name + '.txt', mode='a', encoding='utf-8') as f:
            os.chdir(path)
            f.write(title)
            f.write('\n')
            f.write(text)
            f.tell()
            f.close()
        time.sleep(1)

#随机UA防封
headers = {
            'User-Agent': UserAgent().random
    }

download_web('https://www.biquge.tw/')
