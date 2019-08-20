#!/usr/bin/python
#-*-coding:utf-8-*-

from selenium import webdriver
import time
import sys,os

# -- Help --
# 获取页面元素
# find_element_by_id()
# find_element_by_name()
# find_element_by_class_name()
# find_element_by_tag_name()
# find_element_by_link_text()
# find_element_by_partial_link_text()
# find_element_by_xpath()
# find_element_by_css_selector()

# back()@返回上个页面,Ex:driver.back()
# forward()@前进下个页面
# refresh()@刷新页面
# clear()@清除文本
# send_keys(value)@模拟按键输入
# click()@单击元素
# .title@获取标题
# .text@获取文本
# .current_url@获取当前页面url
# close()@关闭单个窗口
# quit()@关闭所有窗口
# get_screenshot_as_file("file_path/filename")@截图

#鼠标
# 引入 ActionChains 类
# from selenium.webdriver.common.action_chains import ActionChains
# perform()@执行所有ActionChains中存储的行为
# context_click()@右击
# double_click()@双击
# drag_and_drop()@拖动
# move_to_element()@鼠标悬停
# -- Help --


driver = webdriver.Chrome()

#windows
driver.maximize_window()
#driver.set_windows_size(480,800)

#open url
driver.get('http://www.baidu.com')
print(driver.title)

# driver.quit()