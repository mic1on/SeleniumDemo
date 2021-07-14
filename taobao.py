# -*- coding:utf-8 -*-
# @Time : 2021/7/13 14:45
# @Author : MicLon

import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_track(distance, t):  # distance为传入的总距离，a为加速度
    # 加速度
    # 参考来源：https://www.cnblogs.com/xiao-apple36/p/8878960.html
    track = []
    current = 0
    mid = distance * t / (t + 1)
    v = 0
    while current < distance:
        if current < mid:
            a = 3
        else:
            a = -1
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


class ChromeReality:

    def __init__(self):
        # 配置真实浏览器环境
        # self.chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 1. 指定本地浏览器绝对路径
        # self.remote_debugging_port = random.randint(9222, 9999)  # 2. 指定浏览器启动端口
        self.user_data_dir = r'C:\Users\Administrator\Desktop\SeleniumUserData'  # 3. 指定浏览器的UserDataDir
        # 启动真实浏览器
        # subprocess.Popen([
        #     self.chrome_path,
        #     f'--remote-debugging-port={self.remote_debugging_port}',
        #     f'--user-data-dir={self.user_data_dir}'
        # ], shell=True)
        # 初始化浏览器参数以及接管真实浏览器
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # self.chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.remote_debugging_port}")
        self.browser = webdriver.Chrome(options=self.chrome_options)
        # 写入防止检测ChromeDriver
        with open('stealth.min.js') as f:
            js = f.read()

        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })


class SeleniumReality(ChromeReality):

    def __init__(self):
        super(SeleniumReality, self).__init__()
        self.url = 'https://passport.taobao.com/ac/password_find.htm?from_site=0'  # 淘宝找回验证码界面
        self.xiaoji_url = 'https://passport.taobao.com/ac/password_find.htm?from_site=2'  # 淘宝找回验证码界面 小鸡

    def taobao_slider_v1(self):
        '''淘宝滑块'''
        for index in range(1):
            self.browser.get(self.url)
            # 定位滑块元素
            source = self.browser.find_element_by_id("nc_1_n1z")
            # 定义鼠标拖放动作并执行
            # ActionChains(self.browser).drag_and_drop_by_offset(source, 280, 0).perform()
            self.move_right(source, get_track(280, 2))

    def taobao_slider_v2(self):
        '''淘宝小鸡刮刮乐滑块'''
        self.browser.get(self.xiaoji_url)
        # 定位元素
        source = self.browser.find_element_by_id("nc_1_canvas")
        # 加速度调参
        self.move_left_right(source, get_track(480, 2))

    def move(self, slider, tracks, times=1, y_base=0):
        """
        :param slider: 移动的element对象
        :param tracks: 动态移动轨迹
        :param times: 移动次数
        :param y_base: 每次向Y轴多少距离
        :return:
        """
        # 按住对象
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 左右往复计次
        for row in range(times):
            x_now = 0
            for index, x in enumerate(tracks):
                # X轴随移动轨迹值前进
                # Y轴随轮次依次向下
                x_now = x_now + x
                ActionChains(self.browser).move_to_element_with_offset(slider, xoffset=x_now,
                                                                       yoffset=(row + 1) * y_base).perform()
        # 结束后放开鼠标
        ActionChains(self.browser).release(slider).perform()

    def move_right(self, slider, tracks):
        self.move(slider, tracks, times=1, y_base=0)

    def move_left_right(self, slider, tracks):
        self.move(slider, tracks, times=5, y_base=random.randint(15, 20))


if __name__ == '__main__':
    seleniumReality = SeleniumReality()
    # seleniumReality.taobao_slider_v1()
    seleniumReality.taobao_slider_v2()
