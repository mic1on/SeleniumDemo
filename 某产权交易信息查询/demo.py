# -*- coding:utf-8 -*-

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess, random
from parsel import Selector


# base chrome settings
class ChromeReality:

    def __init__(self):
        # 配置真实浏览器环境
        self.chrome_path = r'D:\soft\python38\chromedriver.exe'  # 1. 指定本地浏览器绝对路径
        self.remote_debugging_port = random.randint(9222, 9999)  # 2. 指定浏览器启动端口
        self.user_data_dir = r'C:\Users\Aministrator\Desktop\SeleniumUserData'  # 3. 指定浏览器的UserDataDir
        # 启动真实浏览器
        subprocess.Popen([
            self.chrome_path,
            f'--remote-debugging-port={self.remote_debugging_port}',
            f'--user-data-dir={self.user_data_dir}'
        ], shell=True)
        # 初始化浏览器参数以及接管真实浏览器
        self.chrome_options = Options()
        # self.chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.remote_debugging_port}")
        self.browser = webdriver.Chrome(options=self.chrome_options)


class SeleniumReality(ChromeReality):

    def __init__(self):
        super(SeleniumReality, self).__init__()
        self.js = 'http://www.jsnc.gov.cn/jygg/tzgg/index.html'  # 江苏省农村产权交易信息服务平台
        self.page_num = 2

    def get_js(self):
        self.browser.get(self.js)
        time.sleep(2)
        iframe = self.browser.find_element_by_id('sq')
        # self.browser.switch_to.frame(iframe)  # 切换到iframe中
        # print(self.browser.page_source)  # 打印出iframe中的数据，这些数据经过瑞数加密
        # self.browser.switch_to.default_content()  # 切换回默认浏览器

    def get_pages(self):

        time.sleep(4)
        iframe = self.browser.find_element_by_id('sq')
        self.browser.switch_to.frame(iframe)
        iframe_input = self.browser.find_element_by_xpath('//input[@name="textfield8"]')
        iframe_input.clear()
        iframe_input.send_keys(self.page_num)
        self.page_num += 1

        go_btn = self.browser.find_element_by_xpath('//table[@class="pagesl"]//td[3]/input')
        self.browser.execute_script("arguments[0].click();", go_btn)

        self.browser.switch_to.default_content()

    def crawl(self):
        print('start crawl')
        iframe = self.browser.find_element_by_id('sq')
        self.browser.switch_to.frame(iframe)
        response = Selector(self.browser.page_source)
        proj_nums = response.xpath('//table[@class="show_data"]//tr/td[1]/text()').getall()
        proj_names = response.xpath('//table[@class="show_data"]//tr/td[2]/a/text()').getall()
        reg_locs = response.xpath('//table[@class="show_data"]//tr/td[3]/span/text()').getall()
        reg_dates = response.xpath('//table[@class="show_data"]//tr/td[4]/text()').getall()

        for num, name, loc, date in zip(proj_nums, proj_names, reg_locs, reg_dates):
            item = {}
            item['project_num'] = num
            item['project_name'] = name
            item['reg_loc'] = loc
            item['reg_date'] = date
            print(item)
        self.browser.switch_to.default_content()


if __name__ == '__main__':
    sele_real = SeleniumReality()
    sele_real.get_js()
    while 1:
        sele_real.get_pages()
        sele_real.crawl()
