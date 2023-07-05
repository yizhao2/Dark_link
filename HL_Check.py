import os
import random
import re
import time
import subprocess
import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import openpyxl
import urllib3
urllib3.disable_warnings()


class Checker:
    def __init__(self, spider):
        # 过滤的域名url,人工审核不需要判断的在此填写
        self.filter = ['www.baidu.com']

        # 创建一个 Chrome 浏览器实例，需要下载对应的 ChromeDriver 并配置 PATH 环境变量
        self.driver = None
        self.spider = spider
        self.num = 0
        # 读取 urls.txt 文件中的所有 URL
        with open('urls.txt') as f:
            self.urls = f.read().splitlines()
        # 读取 rules.txt 文件中的所有 规则
        with open('rules.txt') as f:
            self.rules = f.read().splitlines()

        # 打开一个日志文件
        if spider != '1':
            self.excel_obj = openpyxl.Workbook()
            self.ws1 =  self.excel_obj.active
            self.ws1.title = "暗链检测结果"
            self.ws1.append(['序号', '父url', '子url', '扫描开始时间', '扫描结束时间', '是否存在暗链', '结果记录'])

    def clos_file(self):
        # 关闭日志文件
        if self.spider == '2':
            # 文件名+时间
            log_time = time.strftime("_%Y-%m-%d_%H-%M-%S", time.localtime())
            log_filename = './运行结果/暗链排查结果' + log_time + '.xlsx'
            for col in self.ws1.columns:
                max_length = max([
                    len(str(cell.value)) + 0.7 * len(re.findall(r'([\u4e00-\u9fa5])', str(cell.value)))
                    for cell in col
                ])
                self.ws1.column_dimensions[col[0].column_letter].width = (max_length + 2) * 1.2

            self.excel_obj.save(log_filename)
            print('扫描成功，保存目录文件名为' + log_filename)

    def start(self):
        print('开始进行暗链监测')
        self.driver = webdriver.Chrome()
        # 遍历 URL
        self.check_url()
        # 关闭浏览器实例
        self.driver.quit()

    def check_comtent(self, url, html):
        """校验首页暗链"""
        url_list = []
        scan_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            "Content-Type": "text/plain"}

        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if href and "http" in href and 'localhost' not in href:
                url_list.append(href)

        url_list = list(set(url_list))

        for i in url_list:
            response = requests.get(i, headers=headers, verify=False)
            self.log_requests(url, i, response.text, scan_time)

    def check_url(self):
        with open('set_target.txt') as f:
            spi_urls = f.read().splitlines()
        for url in spi_urls:
            scan_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
            # 打开 URL
            if url and "http" in url  and 'localhost' not in url  and url not in self.filter:
                try:
                    self.driver.get(url)
                    # time.sleep(3)
                except selenium.common.exceptions.InvalidArgumentException:
                    self.num += 1
                    end_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
                    self.ws1.append([self.num, url, '', scan_time, end_time, '其他', 'url 格式错误'])
                    continue
                except selenium.common.exceptions.WebDriverException:
                    self.num += 1
                    end_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
                    self.ws1.append([self.num, url, '', scan_time, end_time, '其他', 'url 格式错误'])
                    continue

                # 获取页面 HTML
                html = self.driver.page_source

                # 扫描
                self.log_requests(url, '无', html, scan_time)
                self.check_comtent(url, html)

        # 保存
        self.clos_file()

    def log_requests(self, url, z_url, content,  scan_time):
        end_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        self.num += 1
        flag, content = self.regex_contents(content)
        if flag:
            # message = "[+] " + url + ' ' + content + '\n'
            self.ws1.append([self.num, url, z_url, scan_time, end_time, '检测到暗链', content])
            print('存在暗链！！' + url + '     ' + content)
        else:
            # message = "[-] " + url + ' ' + content + '\n'
            print('无问题过滤   url: ' + url)
            self.ws1.append([self.num, url, z_url, scan_time, end_time, '否', content])

    def regex_contents(self, content):
        value = ''
        for rule in self.rules:
            pattern = re.compile(rule)
            matched = pattern.findall(content)
            if matched:
                value += "[" + matched[0] + " * " + str(len(matched)) + "]"
        if value:
            return True, value
        else:
            return False, "未检测到暗链"


    def radSpider(self):
        file = open("set_target.txt", 'w').close()  # 清理原有内容。重新写入
        for url in self.urls:
            if url and "http" in url and 'localhost' not in url:
                # 先开始爬虫，再逐个遍历检测。
                print('开始爬取目标网站所有页面。')
                scanCommand = "echo {0}| .\httpx.exe -silent -mc 200,301,302 -threads -1000 |.\hakrawler.exe -d 2 -subs > {1}".format(
                    url, "target_domain_js.txt")
                print("\033[1;33m command>>>>>> \033[0m", "\033[1;33m" + scanCommand + "\033[0m")
                finderjs_result = subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                finderjs_result.wait()

                # 鉴于扫出来的文档链接有重复，做一个去重
                with open('target_domain_js.txt', 'r') as f:
                    lines = f.readlines()

                # 对行内容去重
                lines = list(set(lines))

                with open('set_target.txt', 'a') as f:
                    f.writelines(lines)

        print('针对urls.txt目标网站所有链接爬取完毕，保存在本地set_target.txt。')

if __name__ == "__main__":
    print('''                                                  
          $$ |                                                     
 $$$$$$\  $$ |$$\  $$$$$$$\  $$$$$$$\  $$$$$$$\ $$$$$$\  $$$$$$$\  
 \____$$\ $$ |\__|$$  _____|$$  _____|$$  _____|\____$$\ $$  __$$\ 
 $$$$$$$ |$$ |$$\ $$ /      \$$$$$$\  $$ /      $$$$$$$ |$$ |  $$ |
$$  __$$ |$$ |$$ |$$ |       \____$$\ $$ |     $$  __$$ |$$ |  $$ |
\$$$$$$$ |$$ |$$ |\$$$$$$$\ $$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ |  $$ |
 \_______|\__|$$ | \_______|\_______/  \_______|\_______|\__|  \__|
        $$\   $$ |                                                 
        \$$$$$$  |                                                 
         \______/ 
         Author:acitsec.com  V1.0
         注：设置好urls.txt目标网站，以http开头，然后开启爬虫爬取所有页面，再执行暗链监测。
    ''')
    value = input('输入以下选项：\n'
                  '1.输入开启网络爬虫，爬取目标网站所有页面链接，保存到本地文本。\n'
                  '2.执行爬虫回来的所有链接进行敏感字监测。\n'
                  '请输入：  ')
    checker = Checker(spider=value)
    if value == '1':
        checker.radSpider()
    elif value == '2':
        checker.start()
    else:
        print('输入错误，请重新输入！！！！！！！！')