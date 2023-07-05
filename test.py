#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import re
#
# arr = ['.',  '^',  '$',  '*',  '+',  '?',  '{',  '}',  '[',  ']',  '|',  '(',  ')']
# lines = []
# with open('rules_new.txt', 'w') as file:
#     with open('rules.txt', 'r') as f:
#         rules = f.readlines()
#     for s in rules:
#         value = ''
#         for i in s:
#             if i in arr:
#                 value += '\\' + i
#             else:
#                 value += i
#         file.writelines(value)
#
# # print(s)
# # pattern = re.compile(s)
# # print(pattern)
# # matched = pattern.findall('fasiehqwk(安创ehkwq')
# # print(matched)
import openpyxl



# import time
# import openpyxl
# import re
# # 文件名+时间
# log_time = time.strftime("_%Y-%m-%d_%H-%M-%S", time.localtime())
# log_filename = './运行结果/暗链排查结果' + log_time + '.xlsx'
# #
# # # 开始时间与结束时间
# scan_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
# # print(scan_time)
# 
# num = '1'
# url = 'www.test.com'
# exits = '检测到暗链'
# result = '[主权 * 2][党 * 1][妈妈 * 2][灾 * 2][国家安全 * 2][96 * 3][卫星定位 * 2][护法 * 1][妈 * 4][3p * 4][性 * 7][预测 * 2][bt * 2][中国 * 1][ri * 44][比 * 1][av * 54][gn * 9][础 * 1][挑战 * 1]'
# 
# excel_obj = openpyxl.Workbook()
# ws1 = excel_obj.active
# ws1.title = "暗链检测结果"
# end_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
# 
# ws1.append(['序号', '域名或url', '扫描开始时间', '扫描结束时间', '是否存在暗链', '结果记录' ])
# ws1.append([num, url, scan_time, end_time, exits, result])
# # data = sheets.cell(1, 1).value
# for col in ws1.columns:
#     max_length = max([
#         len(str(cell.value)) + 0.7 * len(re.findall(r'([\u4e00-\u9fa5])', str(cell.value)))
#         for cell in col
#     ])
#     ws1.column_dimensions[col[0].column_letter].width = (max_length + 2) * 1.2
# 
# excel_obj.save(log_filename)
# 
# import selenium
# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get('https://life.dayoo.com/auto/202205/26/154616_54273733.htm')
# html = driver.page_source
# print(html)
# driver.quit()

def check_comtent():
    """校验首页暗链"""
    try:
        scan_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        for url in self.urls:
            # 获取网站首页内容
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            #
            # 获取所有链接
            links = soup.find_all("a")
            # 遍历所有链接，检查是否存在暗链

            for link in links:
                href = link.get("href")
                if href and "http" in href and 'localhost' not in href:
                    print('存在的暗链：' + href)
                    # 延缓读取速度，避免当成爬虫被封IP
                    # time.sleep(1)
                    response = requests.get(href, headers=headers)
                    # log_requests(href, response.text, 'html', scan_time)
    except Exception as e:
        print('错误：', e)

# driver = webdriver.Chrome()
# driver.get('https://life.dayoo.com/auto/202205/26/154616_54273733.htm')
# html = driver.page_source

# import os
# import random
# import re
# import time
# import subprocess
# import requests
# import selenium
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import requests
# import openpyxl



# headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#             "Content-Type": "text/plain"}
# response = requests.get('https://life.dayoo.com/auto/202205/26/154616_54273733.htm', headers=headers, verify=False)
# response.encoding = 'utf-8'
# text = response.content.decode('utf-8')
# # print(text)
#
# with open('新建文本文档.txt', 'w', encoding='utf-8') as f:
#     val = f.write(text)
#
#
# if '3p' in text:
#     print('3p在')
# if 'jb' in text:
#     print('jb')
#
# if text.find('3p'):
#     print('find 3p')
# if text.find('jb'):
#     print('find jb')
#
# rules = ['3p', 'jb', 'gb', '热评']
# value = ''
# for i in rules:
#     search_string = re.escape(i)
#     pattern = re.compile(search_string)
#     matched = pattern.findall(text)
#     print(matched)
#     if matched:
#         value += "[" + matched[0] + " * " + str(len(matched)) + "]"
# print(value)
#

# value = re.findall(r'\d', s)
# import tldextract

# url = 'https://news.dayoo.com/society/140000.shtml'
#
# extracted = tldextract.extract(url)
# domain = extracted.domain + '.' + extracted.suffix

# print(domain)
# s = ['dayoo.com', 'sszz.com', '123ae.com']
# url = 'https://news.dayoo.com/society/140000.shtml'
# if any(domain in url for domain in s):
#     print('有匹配的项')
# else:
#     print('没有匹配的项')





# print(response.text)
# soup = BeautifulSoup(response.content, "html.parser")
# soup = BeautifulSoup(html, "lxml")
#
# 获取所有链接
# links = soup.find_all("a")
# link_url = soup.find_all("link")
# s_url = soup.find_all("script")
# print(links)
# url_list = []
# for link in links:
#     href = link.get('href')
#     if href and "http" in href and 'localhost' not in href:
#         url_list.append(href)
#
# url_list = list(set(url_list))
# print(url_list)
# driver.quit()
# for i in url_list:


import requests
import json
import urllib3
urllib3.disable_warnings()


def get_token(keyword):
    url = 'https://trends.google.com/trends/api/explore?hl=zh-CN&tz=-480&req={"comparisonItem":[{"keyword":"Garmin+Golf","geo":"US","time":"today+12-m"}],"category":18,"property":""}&tz=-480'
    print(url)

    headers = {
        'authority': 'trends.google.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'HSID=Aw0lQQUdEpv9bj41C; SSID=AXzXvaiMUknwO3HBi; APISID=GBZFr85wm5RTk4gJ/A5F5Q5vvlOU5xaSyO; SAPISID=ZwRUPJJ9Cr9Yi3Mz/AZzOxtuPv0NWobt2F; __Secure-1PAPISID=ZwRUPJJ9Cr9Yi3Mz/AZzOxtuPv0NWobt2F; __Secure-3PAPISID=ZwRUPJJ9Cr9Yi3Mz/AZzOxtuPv0NWobt2F; AEC=AUEFqZf3PCacBRSlf7pUPcJK3wIFsnLXI61MX_RSAEUpeJwZbWS7nUT5UYc; 1P_JAR=2023-05-29-10; NID=511=QUAKR0X2g0oHM9As_rGlGkgpPlffBoSab3iQh6FXmNcYRTIge4NAx_FJtmAeOM6kijqMxFhHbrK_b3LMo3nYlaE5iLjMuO5l4PBMKbFDKu-p2qHmfGeahZonvWDZaIMZvuc7iR82QAiKyJy2PpNloMR39JwKSi2IIKj6ok_wvvW1a6ZySD5vO-d1FlRkZDqv66N4FKc3e0MKpByPRDBgaKeZvDhyKLoWqEk9oqI-csyhCnbGaJTfHG0YVsRTH41ixL8Zh-kM1cbvyw80Yja-XKs; SID=[SC]CgUN_8MAAJoGDENBRVFBeGpPbUFFPaIGmQEAhqprYu_L5tNRdCvoKu2htD5KAjaoJrqv3RbSKTAiFRRS0UbksZEjKKnedNo3q1t2kDjW2q8ZSd2q9sp_uc0mll7MdmXKbCb879GLJryS1Y4hZ5bYajOpQVywmZDR23P44j59kdaZXKZ8m7cNrl5tt_vwYdr9AOUbUJnyxi71WCRdHAByR4626CsZ0ml2sidwi1iYrtQH0x2qBoABZThmOTkxYzE3NzEzMmMxYzJkMjUyMTliN2ViZjBmNmYyNDMzMGI4NTk1MjA2M2RlMjliZDVkYzJkYzIxODcwODhmMjU5N2FjNDdmNDA5OTkxODk2YTA0MmZhMzUzYjc4NTkyNWRmNGM3MDU1ODk3NWI0NjZjODI4MWE5OTlhOWM; __Secure-1PSID=[SC]CgUN_8MAAJoGDENBRVFBeGpPbUFFPaIGmQEAhqprYs2nGnflU1MQ4yYKhR24GIPxGHgfdjR0Ny2Le5fRfkbk72SLJRTNu2TREwxuRGXeLX7bLDDYW0zHC2DJHHN5uZyO1Si22AxGFIghEZga_tyaeyQcbMzlOPiytpyUILOTVm9ng6QFxai2AOrBQZJBYziTxF_doKnQ53uGXTrnF6FvYnEpBCnMdv-TLcST3o244Z6GpKmqBoABYzg2MWE4MGE5OGIzNzExYzdkMWU5N2ZkNjg2YmIzOGEzMjFhYjIzODI3NjYwZmRmNWEyYTA1YTllNmU4OTA0N2Y5YTNiYWMzMTIxNzAxNTQ0ZTJhYmJkZTU0MTRlOWNhYjFiZTcwYWVhNTJlMDFjYjQ1NTE1MWU3NzYyMjkwOWQ; __Secure-3PSID=[SC]CgUN_8MAAJoGDENBRVFBeGpPbUFFPaIGmQEAhqprYvZ5Lf9zqLKKnGsdn_ZHD6uoZFs_oZctNl6HUBYgwRk_MMSZbUg3mlTZRA2BK4tO-0qzZGw-GUwDO3H9DBwg-rTVnxli-6fQ4NKduIj9yPQNmAUOeA8JWNsTXBi3PM4IIIwbqrsaRPnYZrnugAk2FDJzl876acPI9Hh4yfbLdLq5nOIzmPv9tRUHucFZpw-r80_Cx7uqBoABN2I1NDA0MWE4OGE3YWQwYjZjOGIyNTdlNTk3NDdhZmI0MDIwYWZmMjhmMzk1NzkwZjc4MGVlN2MwMjY1YjBlYzExZjRhMmYyZDZiZDMyNDAyMDNjMDNlNDVhOGNhYWY1NzhmN2M3MDNmNGNjMTg4NWFkNWM1MzQwMjY0ZmZlNGY; SIDCC=AP8dLtxnCqRqeELPSQxfrRZHIQ_K2mYIhQIDW5cWrKb58IZm1u5L9HyPyPBAMESsw_gIYHKLDg; __Secure-1PSIDCC=AP8dLtzZHS-j9gE4QZ_Fq2smWG5xkyo8pynOO4VCmw7uhNYxEVyeG3n9VPiMWMKszP_YGV6-iYw; __Secure-3PSIDCC=AP8dLtzR6vHjvWy4vni2KfW2mwwBVLpxzju6pHYuvKrZ2p5R91ckqJRSGofgeUEj_lBDGmxxhmM',
        'origin': 'https://trends.google.com',
        'referer': 'https://trends.google.com/trends/explore',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.105", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }



    proxy_url = 'http://szzhcxkj:8c12a2-b80516-2afde9-c0695b-452679@unmetered.residential.proxyrack.net:12541'
    proxies = {
        "http": None,
        "https": None
    }
    try:
        response = requests.request("POST", url, headers=headers, proxies=proxies,   verify=False)
    except:
        response = requests.request("POST", url, headers=headers,  proxies=proxies,  verify=False)
    print(response)

    # response = session.request("POST", url, headers=headers, proxies=proxies, verify=False)

    print(response.text)

if __name__ == '__main__':
    keyword = 'Garmin Golf'
    word_list = [x for x in keyword.split(' ') if x]
    format_word = '+'.join(word_list)
    get_token(format_word)



