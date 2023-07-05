import os
import random
import re
import time
import subprocess
import requests
from bs4 import BeautifulSoup
import requests
import openpyxl
import urllib3
import tldextract
urllib3.disable_warnings()


class Checker:
    def __init__(self, spider):
        # 过滤的域名url,人工审核不需要判断的在此填写
        self.filter = ['www.baidu.com']
        self.spider = spider
        self.num = 0
        self.z_url = ''
        self.domain_list = []
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
            self.ws1.append(['序号', '父网站', '隐藏的url', '扫描开始时间', '扫描结束时间', '是否识别到敏感词', '结果记录'])

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

    def start(self):

        self.check_comtent()

    def check_comtent(self):
        """校验爬出来的网站所有的暗链"""
        self.domain_list = self.get_domain()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            "Content-Type": "text/plain"}
        with open('set_target.txt') as f:
            spi_urls = f.read().splitlines()
        set_url_list = []
        for url in spi_urls:
            if url and "http" in url and 'localhost' not in url and url not in self.filter:
                scan_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
                try:
                    url_list = []
                    # 获取网站首页内容
                    # 第一个元素表示连接超时时间，第二个元素表示读取超时时间。
                    try:
                        response = requests.get(url, headers=headers, verify=False, timeout=(5, 10))
                    except requests.exceptions.Timeout:
                        # 处理连接超时异常
                        print("连接超时异常", url)
                        continue
                    except requests.exceptions.ConnectionError:
                        # 处理连接错误异常
                        print("连接错误异常", url)
                        continue
                    soup = BeautifulSoup(response.content, "html.parser")
                    # 扫描该网站
                    self.log_requests(url, '', response.text, scan_time)
                    # 获取所有链接 a标签，link标签通常用于导入css样式表，script通常导入js链接脚本，无需获取
                    links = soup.find_all("a")

                    for link in links:
                        href = link.get("href")
                        if href and "http" in href and 'localhost' not in href and href not in self.filter:
                            url_list.append(href)
                            # 延缓读取速度，避免当成爬虫被封IP
                            # time.sleep(1)

                    url_list = list(set(url_list))

                    for i in url_list:
                        if i not in set_url_list:
                            scan_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
                            self.z_url = i
                            try:
                                response = requests.get(i, headers=headers, verify=False, timeout=(5, 10))
                            except requests.exceptions.Timeout:
                                # 处理连接超时异常
                                print("子域名连接超时异常", i)
                                continue
                            except requests.exceptions.ConnectionError:
                                # 处理连接错误异常
                                print("子域名连接错误异常", i)
                                continue
                            self.log_requests(url, i, response.text, scan_time)

                    set_url_list += url_list

                except Exception as e:
                    self.num += 1
                    end_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
                    self.ws1.append([self.num, url, self.z_url, scan_time, end_time, '错误！', str(e)])
                    continue

        self.clos_file()

    def log_requests(self, url, z_url, content, scan_time):
        end_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        self.num += 1
        flag, content = self.regex_contents(content)
        if flag:
            last_url = z_url if z_url else url

           # 通过url.txt获取主域名，从而判断是否本站的外链，因为通常本站出现问题几率小，都是外站的外链问题多，增加提示，方便用户查看了解。
            if any(domain in last_url for domain in self.domain_list):
                self.ws1.append([self.num, url, z_url, scan_time, end_time, '检测到敏感词', content])
                print('本站检测到敏感词！ ' + last_url + '     ' + content)
            else:
                self.ws1.append([self.num, url, z_url, scan_time, end_time, '外链检测到敏感词', content])
                print('！！！存在外站外链敏感词' + last_url + '     ' + content)

        else:
            self.ws1.append([self.num, url, z_url, scan_time, end_time, '否', content])

    def get_domain(self):
        """获取主域名判断"""
        domain_list = []
        for url in self.urls:
            extracted = tldextract.extract(url)
            domain = extracted.domain + '.' + extracted.suffix
            domain_list.append(domain)
        return domain_list

    def regex_contents(self, content):
        """过滤识别敏感词"""
        value = ''
        for rule in self.rules:
            pattern = re.compile(rule)
            matched = pattern.findall(content)
            if matched:
                value += "[" + matched[0] + " * " + str(len(matched)) + "]"
        if value:
            return True, value
        else:
            return False, "未检测到敏感词"

    def clos_file(self):
        # 保存excel结果
        if self.spider == '2':
            # 文件名+时间
            log_time = time.strftime("_%Y-%m-%d_%H-%M-%S", time.localtime())
            log_filename = './运行结果/暗链排查结果' + log_time + '.xlsx'
            for col in self.ws1.columns:
                max_length = max([
                    len(str(cell.value)) + 0.7 * len(re.findall(r'([\u4e00-\u9fa5])', str(cell.value)))
                    for cell in col
                ])
                self.ws1.column_dimensions[col[0].column_letter].width = (max_length + 2) * 1.1

            self.excel_obj.save(log_filename)
            print('扫描成功，保存目录文件名为' + log_filename)


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