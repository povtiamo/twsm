'''
 * @Author: lijiayi 
 * @Date: 2019-06-28 14:40:14 
 * @Last Modified by:   lijiayi 
 * @Last Modified time: 2019-06-28 14:40:14 
'''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

import sys
import os
import requests
import time
import datetime
import json
import urllib
import urllib.parse
import base64
import traceback
# import threading
import uuid
import re
import hashlib
# from Crypto.Cipher import AES


class base():
	#设置重连次数
	requests.adapters.DEFAULT_RETRIES = 15
	# 设置连接活跃状态为False
	s = requests.session()
	s.keep_alive = False

	def __init__(self,IP=None,PORT=None,username=None,filename=None,file=None,activityName=None,times=None):
		self.userId=0
		self.realName=''
		self.orgName=''
		self._uuid_1=''.join(str(uuid.uuid4()).split('-'))	#split去除符号“-”
		self.headers={
		"Accept":"*/*",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
		}
		self.IP=IP
		self.PORT=PORT
		self.index=str(IP)+":"+str(PORT)
		self.username=username
		self.password="123456"
		self.filename=filename
		self.file=file
		self.activityName=activityName
		self.times=times

	def main(self):
		pass

	def getHTTP(self,uri,params=None,headers=None,cookies=None,timeout=30):
		if not headers:
			headers=self.headers
		result=requests.get(url=uri,params=params,headers=headers,cookies=cookies,timeout=timeout)	#带参数的get,get方法param拼接在链接后面
		return result

	def postHTTP(self,uri,params=None,data=None,files=None,headers=None,cookies=None,timeout=60):
		if not headers:
			headers=self.headers
		# print(uri,data)
		result=requests.post(url=uri,params=params,data=data,files=files,headers=headers,cookies=cookies)
		return result

	def optionsHTTP(self,uri,params=None,data=None,files=None,headers=None,cookies=None,timeout=30):
		if not headers:
			headers=self.headers
		result=requests.options(url=uri,params=params,data=data,files=files,headers=headers,cookies=cookies)
		return result

	def ResultTextConvert(self,result):
		try:
			return json.loads(result.text.encode('utf-8'))
		except:
			return result.text.encode('utf-8')

	def timeStamp(self):
		#timeStamp=time.time()	#当前时间戳，为float类型
		#date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))	#'20xx-xx-xx xx:xx:xx'
		timeStamp=int(round(time.time()*1000))	#round()是四舍五入,timeStamp获取13位数时间戳
		return timeStamp

	def getFileMD5(self,file_path):
		with open(file_path,"rb") as file:
			filemd5=hashlib.md5(file.read()).hexdigest()#get 32 value
		return filemd5

	def To_sha256(self,data):
		result = hashlib.sha256(data.encode('utf-8')).hexdigest()
		return result

	# def To_AES_base64(self,data,key):#加密时使用的key，只能是长度16,24和32的字符串
	# 	# 设置block_size的大小为16
	# 	BS =AES.block_size
	# 	mode=AES.MODE_CBC
	# 	key=key.encode('utf-8')	#key to bytes
	# 	data=data.encode('utf-8')
	# 	aes=AES.new(key,mode,b'0000000000000000')
	# 	#对内容自动补全16位，填充内容是“16-len(s)”对应的ascii字符
	# 	#chr(int)返回数字的ascii码，ord(str)返回字符的ascii码
	# 	#lambda匿名函数sum=lambda s:s+1->def sum(s):return s+1
	# 	#data[0:-1]data从后往前减一个值，a="123";a[0:-1]="12"
	# 	DataConvert=lambda s:s+(BS-len(s)%BS)*chr(BS-len(s)%BS)
	# 	data=DataConvert(data)
	# 	result =self.To_Base64(result)
	# 	return result

	def To_Base64(self,*args):	# *args is (1,2) **kw is a=1,b=2
		try:
			#base64.b64decode 解码
			data_list=[]
			for data in args:
				data=base64.b64encode(data.encode('utf-8')) #base64加密
				data=str(data,"utf-8")	#byte格式转成str，去掉b''
				data_list.append(data)
			if len(data_list)==1:
				return data_list[0]
			elif len(data_list)==0:
				return args
			else:
				return data_list
		except Exception:
			print("error：*args must be string or try->(func.To_Base64(\"1\",\"2\")")

	def To_Base64_decode(self,data):
		data=base64.b64decode(data)
		return data

	def file_To_Base64(self,file_path):
		with open(file_path,"rb") as file:
			_file=base64.b64encode(file.read()).decode()
		return _file

	def _urlencode(self,data):
		try:
			result=urllib.parse.urlencode(data)	#URL编码，json格式
			return result
		except:
			result=urllib.parse.quote(data)	#URL编码，字符串格式
			return result

	def _urldecode(self,data):
		try:
			result=urllib.parse.unquote(data)
			return result
		except:
			return data
			
	def getUUID5(self):
		return ''.join(str(uuid.uuid4()).split('-'))	#split去除符号“-”

	def showResult(self,data):
			print("recv<<\n%s"%(data))

if __name__=='__main__':
	b=base()
	# _str="loginId①01②staticmm①MTIzNDU2②schoolId①null"
	# code=b._urlencode(_str)
	# print(code)
	# code=b.To_Base64(code)
	# print(code)

	# code=b.To_Base64_decode("bG9naW5JZCVFMiU5MSVBMDAxJUUyJTkxJUExc3RhdGljbW0lRTIlOTElQTBNVEl6TkRVMiVFMiU5MSVBMXNjaG9vbElkJUUyJTkxJUEwbnVsbA==")
	# code=str(code,'utf-8')
	# code=urllib.parse.unquote(code)
	#print(code)
	file_path="C:\\C_workscpace\\test\\test_rename.txt"
	md5=b.getFileMD5(file_path)
	print(md5)