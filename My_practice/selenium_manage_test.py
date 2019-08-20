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
_DEBUG=False

class Client():
	def __init__(self,username,password):
		self.__username = username
		self.__password = password
		self.__element_username = "username"
		self.__element_password = "passowrd"
		self.__element_verify = ""
		self.__element_Loginclick = "icon-key"
		self.__element_Loginresult = "alert-danger"
		self.__element_ItemList = ""
		self.__element_ItemFind = ""
		self.__driver = ''

	def login(self):
		if _DEBUG is True:
		    import pdb
		    pdb.set_trace()

		#open Chrome
		driver = webdriver.Chrome()
		self.__driver = driver
		#windows
		driver.maximize_window()
		#driver.set_windows_size(480,800)

		#open url
		driver.get('http://www.baidu.com')
		print driver.title

		# driver.find_element_by_name(self.__element_username).send_keys(self.__username)
		# print"input username \"%s\""%(self.__username)
		# time.sleep(1)

		# driver.find_element_by_name(self.__element_password).send_keys(self.__password)
		# print "input password \"%s\""%(self.__password)
		# time.sleep(1)

		# self.__element_verify=raw_input("input verify >")
		# driver.find_element_by_name("verify").send_keys(self.__element_verify)
		# print "input verify \"%s\""%(self.__element_verify)
		# time.sleep(1)

		# driver.find_element_by_class_name(self.__element_Loginclick).click()
		# print "click login"

		# try:
		# 	return_msg = driver.find_element_by_class_name(self.__element_Loginresult).text
		# 	print "login result:%s"%(return_msg)
		# except:
		# 	print "login succes!"
		# 	pass

		# self.find_Item()

		# self.__del__()
		

	def find_Item(self):
		pass

	def __del__(self):
		time.sleep(1)
		self.__driver.quit()

try:
	if __name__ == '__main__':
		user=raw_input("input username >")
		passwd=raw_input("input password >")
		c = Client(user,passwd)
		c.login()

except KeyboardInterrupt:
    print "key break!"
    c.__del__()
    pass

finally:
    print "program Finish!"
    sys.exit()
