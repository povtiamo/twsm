#!/usr/bin/python
#-*-coding:utf-8-*-

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

#Select下拉框
# 通过index进行选择
#Select(driver.find_element_by_name("form:j_idt163")).select_by_index(1)
# 通过value进行选择
#Select(driver.find_element_by_name("form:j_idt163")).select_by_value("TEST")
# 通过选项文字进行选择
#Select(driver.find_element_by_name("form:j_idt163")).select_by_visible_text("TEST")

#鼠标
# 引入 ActionChains 类
# from selenium.webdriver.common.action_chains import ActionChains
# perform()@执行所有ActionChains中存储的行为
# context_click()@右击
# double_click()@双击
# drag_and_drop()@拖动
# move_to_element()@鼠标悬停

#By方法
# ID = "id"
# XPATH = "xpath"
# LINK_TEXT = "link text"
# PARTIAL_LINK_TEXT = "partial link text"
# NAME = "name"
# TAG_NAME = "tag name"
# CLASS_NAME = "class name"
# CSS_SELECTOR = "css selector"
# -- Help --

from selenium import webdriver
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys,os
import traceback


class Client():
	def __init__(self,username,password,runtimes):
		self.__username = username
		self.__password = password
		self.runtimes=runtimes
		self.__element_username = "username"
		self.__element_password = "passowrd"
		self.__element_verify = ""
		self.__element_Loginclick = "icon-key"
		self.__element_Loginresult = "alert-danger"
		self.__element_ItemList = ""
		self.__element_ItemFind = ""
		self.__driver=''
		self.uri_index="http://192.168.130.59/#/"

	def main(self):
		self.index()
		self.login()
		# self.sign(1)
		for i in range(int(self.runtimes)):
			try:
				self.add_child(i)
				# self.sign(i)
			except KeyboardInterrupt:
				print("key break!")
				break
			except Exception:
				continue
		self.__driver.quit()

	def open_boxer(self):
		#open Chrome
		driver=webdriver.Chrome()
		self.__driver = driver

	def open_windows(self):
		#windows
		self.__driver.maximize_window()
		#driver.set_windows_size(480,800)

	def index(self):
		self.open_boxer()
		self.open_windows()
		#open url
		self.__driver.get(self.uri_index)
		print(self.__driver.title)

	def login(self):
		self.__driver.find_element_by_link_text("登录").click()
		self.__driver.find_element_by_xpath("//*[@class='el-form']/div[1]/div[@class='el-form-item__content']/div/input").send_keys(self.__username)
		self.__driver.find_element_by_xpath("//*[@class='el-form']/div[2]/div[@class='el-form-item__content']/div/input").send_keys(self.__password)
		verify=input("input verify>")
		self.__driver.find_element_by_xpath("//*[@class='el-form']/div[3]/div[@class='el-form-item__content']/div/input").send_keys(verify)
		self.__driver.find_element_by_xpath("//*[@class='mb-tiny']/a").click()
		#self.__driver.refresh()
		time.sleep(3)
		#until(method, message='')	调用该方法提供的驱动程序作为一个参数，直到返回值不为 False。
		#until_not(method, message='')	调用该方法提供的驱动程序作为一个参数，直到返回值为 False。
		#WebDriverWait等设置等待时间和超时时间
		#WebDriverWait(self.__driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME,"tw-modal-window-footer")))#is_displayed()、is_enabled()、is_selected()
		#WebDriverWait(self.__driver, 10).until(lambda x:x.find_element_by_xpath("//*[@class='tw-modal-window-footer']/a[1]").click())#is_displayed()、is_enabled()、is_selected()
		self.__driver.find_element_by_xpath("//*[@class='tw-modal-window-footer']/a[1]").click()

	def add_child(self,userindex):
		time.sleep(2)
		self.__driver.find_element_by_xpath("//*[@class='tw-title']/div[1]/a[1]").click()
		time.sleep(1)
		#学段
		#证件类型
		#证件号
		# r1=self.__driver.find_element_by_xpath("//*[@class='tw-body-content']/form/div[4]/div[2]/div[3]")
		# r2=r1.find_element_by_xpath(".//div/div/input").send_keys("1")
		self.__driver.find_element_by_xpath("//*[@class='tw-body-content']/form/div[4]/div[2]/div[3]/div/div/input").send_keys(self.get_cardNo(userindex))
		#学生姓名
		self.__driver.find_element_by_xpath("//*[@class='tw-body-content']/form/div[4]/div[2]/div[4]/div/div/input").send_keys(self.get_stuName(userindex))
		#学生曾用名
		#self.__driver.find_element_by_xpath("//*[@class='tw-body-content']/form/div[4]/div[2]/div[5]/div/div/input").send_keys()
		#学生关系
		self.__driver.find_element_by_xpath("//*[@class='el-form xmedium ml-huge']/div[4]/div[2]/div[6]/div/div/div[1]").click()#点击列出下拉框代码
		time.sleep(1)
		ul = self.__driver.find_element_by_css_selector("[x-placement='top-start']>div>div>ul")#用css查找其他属性值
		#ul.find_element_by_xpath(".//li").extract()[2].click()
		itemlist=ul.find_element_by_xpath(".//li[@class='el-select-dropdown__item']")#.//相对路劲
		itemlist.find_element_by_xpath(".//span").click()
		time.sleep(1)
		#提交
		self.__driver.find_element_by_xpath("//*[@class='el-form xmedium ml-huge']/div[@class='el-form-item el-form-item--small']/div/a").click()
		self.__driver.find_element_by_xpath("//*[@class='el-message-box__btns']/button[2]").click()
		time.sleep(2)
		self.__driver.refresh()

	def get_cardNo(self,userindex):
		cardNo="43252220020101%04d"%(int(userindex))
		return cardNo

	def get_stuName(self,userindex):
		dic={"0":u"零","1":u"壹","2":u"贰","3":u"叁","4":u"肆","5":u"伍","6":u"陆","7":u"柒","8":u"扒","9":u"玖"}
		realName="政策生"
		for x in str(userindex):
			realName+=dic[x]
		return realName

	def sign(self,userindex):
		time.sleep(2)
		self.__driver.find_element_by_xpath("//*[@class='tw-tabs xnoborder xinline']/li[3]/a").click()
		self.__driver.find_element_by_xpath("//*[@class='tw-collapse xopen']/div/div[2]/a").click()
		self.__driver.find_element_by_xpath("//*[@class='el-form-item is-required el-form-item--small'][1]/div/div/div[2]/a").click()
		self.__driver.find_element_by_xpath("//*[@class='el-form-item is-required el-form-item--small'][2]/div/div/a[2]").click()
		self.__driver.find_element_by_xpath("//*[@class='tw-fixbtns']/a[2]").click()
		self.__driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div/div[2]/form/div[1]/div[2]/div/div").click()



	# def __del__(self):
	# 	time.sleep(1)
	# 	self.__driver.quit()

try:
	if __name__ == '__main__':
		user='13662539542'
		passwd='123456'
		runtimes="100"
		c = Client(user,passwd,runtimes)
		c.main()

except KeyboardInterrupt:
    print("key break!")
    # c.__del__()
    pass
