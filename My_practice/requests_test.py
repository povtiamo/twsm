#!/usr/bin/python
#-*-coding:utf-8-*-

import sys,os
import requests
import time
import json
import urllib
import urllib.parse
import base64
import traceback
import threading
import uuid
import re


class client():
	def __init__(self,IP,PORT,username,filename,file,activityName):
		self.userId=0
		self.realName=''
		self.orgName=''
		self.IP=IP
		self.PORT=PORT
		self.index=str(IP)+":"+str(PORT)
		self.username=username
		self.password="123456"
		self.filename=filename
		self.file=file
		self.activityName=activityName
		self.search_key="活动"
		self.login_cookies=""
		self.index_path="/activityzone/activity/index"
		self.search_activity_path="/activityzone/activity/queryData?_="
		self.login_path="/activityzone/login/commonLogin"
		self.logout_path="/activityzone/login/logout"
		self._headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
		self._uuid_1=''.join(str(uuid.uuid4()).split('-'))	#split去除符号“-”
		self.upload_path="/activityzone/api/uploadfile/webuploader?uuid=%s&name=%s&id=WU_FILE_0&type=application%%2Foctet-stream&lastModifiedDate=Thu+Apr+11+2019+15%%3A02%%3A45+GMT%%2B0800+(%%E4%%B8%%AD%%E5%%9B%%BD%%E6%%A0%%87%%E5%%87%%86%%E6%%97%%B6%%E9%%97%%B4)&size=224875"%(self._uuid_1,self.filename)
		self.upload_data=""
		self.CreateActivity_path="/activityzone/activity/save?_="
		self.notice_path="/activityzone/notice/update"

	def main(self):
		self.getHTTP("http://%s%s"%(self.index,self.index_path))

		search_param=self.search_activity("",self.To_Base64(self.search_key),"5") #状态；搜索字；显示数量
		search_activity_result=self.getHTTP("http://%s%s%s"%(self.index,self.search_activity_path,self.timeStamp()),search_param)
		self.search_showResult(search_activity_result)

		login_result=self.getHTTP("http://%s%s"%(self.index,self.login_path),self.getlogininfo())
		self.showResult(login_result)
		self.login_cookies=self.GETcookies("http://%s%s"%(self.index,self.login_path),self.getlogininfo())
		self.login_cookies={"JSESSIONID":"%s"%(self.login_cookies)}

		upload_result=self.fileupload("http://%s%s"%(self.index,self.upload_path),self.upload_data,self.file,cookies=self.login_cookies)
		self.showResult(upload_result)
		localPath=upload_result["localPath"]
		self.getHTTP("http://%s/dls/download//%s"%(self.index,localPath),cookies=self.login_cookies)

		# notice_result=self.postHTTP("http://%s%s"%(self.index,self.notice_path),self.getnoticeMSG(upload_result))
		# self.showResult(notice_result)

		creat_headers={"Accept":"application/json, text/javascript, */*; q=0.01","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36","X-Requested-With":"XMLHttpRequest","Content-Type":"application/json"}
		create_result=self.postHTTP("http://%s%s%s"%(self.index,self.CreateActivity_path,self.timeStamp()),self.getCreateActivityMSG(upload_result),creat_headers,self.login_cookies)
		self.showResult(create_result)

		self.getHTTP("http://%s%s"%(self.index,self.logout_path),cookies=self.login_cookies)

	def getHTTP(self,URI,param=None,headers=None,cookies=None):
		print("GET>>\n",URI,cookies)
		getHTTP_result=requests.get(url=URI,params=param,headers=self._headers,cookies=cookies)	#带参数的get,get方法param拼接在链接后面
		try:
			return json.loads(getHTTP_result.text.encode('utf-8'))
		except:
			print(">not json<\n")
			return getHTTP_result.text.encode('utf-8')

	def GETcookies(self,URI,param=None,headers=None,cookies=None):
		getHTTP_result=requests.get(url=URI,params=param,headers=self._headers,cookies=cookies)
		print("Get cookies:",getHTTP_result.cookies["JSESSIONID"])
		return getHTTP_result.cookies["JSESSIONID"]

	def postHTTP(self,URI,data,headers=None,cookies=None):
		print("POST>>\n",URI,data,cookies)
		postHTTP_result=requests.post(url=URI,data=data,headers=headers,cookies=cookies)
		try:
			return json.loads(postHTTP_result.text.encode('utf-8'))
		except:
			print(">not json<\n")
			return postHTTP_result.text.encode('utf-8')

	def fileupload(self,URI,param,files,headers=None,cookies=None):
		headers={"Accept-Language":"zh-CN,zh;q=0.9","Content-Type":"image/jpeg","Accept-Encoding":"gzip, deflate","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36","Accept":"*/*"}
		print("UPLOAD>>\n",URI,param,files,cookies)
		postHTTP_result=requests.post(URI,param,files=files,headers=headers,cookies=cookies)
		try:
			return json.loads(postHTTP_result.text.encode('utf-8'))
		except:
			print(">not json<\n")
			return postHTTP_result.text.encode('utf-8')

	def timeStamp(self):
		#timeStamp=time.time()	#当前时间戳，为float类型
		#date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))	#'20xx-xx-xx xx:xx:xx'
		timeStamp=int(round(time.time()*1000))	#round()是四舍五入,timeStamp获取13位数时间戳
		return timeStamp

	def getlogininfo(self):
		username=self.username
		password=self.To_Base64(self.password)
		logininfo="n=%s&p=%s&loginUser=&childId=&targetUrl=&validCode=&appId=&interfacesURL=undefined"%(username,password)
		logininfo=self.To_Base64(logininfo)
		logininfo=self._urlencode({"loginInfo":logininfo})
		#print("test:",self.To_Base64("1","2"))
		return logininfo

	def getnoticeMSG(self,fileinfo):
		filejson={"localPath":fileinfo["localPath"],
			"fileUrl":fileinfo["fileUrl"],
			"fileName":fileinfo["fileName"],
			"size":fileinfo["fileSize"],
			"fileSize":fileinfo["fileSize"],
			"format":fileinfo["format"],
			"type":fileinfo["type"]}
		noticeMSG={
			"title":"123",
			"file":"",
			"fileJson":filejson,
			"type":"0",
			"orderNo":"3",
			"creator":"CY00039600000000009",
			"viewNum":"21",
			"id": "CY00039300000000011",
			"status":"0",
			"content":"<p>qwe</p>"}
		noticeMSG=self._urlencode(noticeMSG)
		return noticeMSG

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
			print("error：*args must be string or tyr->(self.To_Base64(\"1\",\"2\")")

	def _urlencode(self,data):
		try:
			data_encode=urllib.parse.urlencode(data)	#URL编码，json格式
			return data_encode
		except:
			data_encode=urllib.parse.quote(data)	#URL编码，字符串格式
			return data_encode

	def search_activity(self,activityStatus,keyword,numPerPage):
		search_activity_json={
		"activityStatus":activityStatus,
		"keyword":keyword,
		"numPerPage":numPerPage}
		search_activity_json=urllib.parse.urlencode(search_activity_json)
		return search_activity_json

	def search_showResult(self,search_activity_result):
		if search_activity_result["serverResult"]["resultCode"]==0:
			try:
				print("recv<<\n")
				for r in search_activity_result["result"]["dataList"]:
					print("activityId：",r["activityId"])
					print("activityName：",r["activityName"])
			except:
				self.showResult(search_activity_result)
		else:
			print("error:%s"%(search_activity_result))

	def showResult(self,data):
		try:
			self.userId=data["userInfo"]["userId"]
			self.realName=data["userInfo"]["realName"]
			self.orgName=data["userInfo"]["orgName"]
			print("recv<<\nuserId:%s,\nuserInfo:%s,\norgName:%s"%(self.userId,self.realName,self.orgName))
		except Exception:
			# traceback.print_exc()
			print("recv<<\n%s"%(data))

	def getCreateActivityMSG(self,fileinfo):
		msg=""
		with open("D:\\Python\\My_practice\\CreateActivity_msg.txt","rb") as f:
			msg=f.read().decode('utf-8')
			# msg=re.split("\\n|\\t|\\r",msg)	#re.split同时分隔msg中的\n\t\r
			msg=json.loads(msg)
			msg["managerList"][0]["userId"]=self.userId
			msg["coverPath"]=fileinfo["localPath"]
			msg["backgroundPath"]=fileinfo["localPath"]
			msg["managerList"][0]["realName"]=self.realName
			msg["managerList"][0]["orgName"]=self.orgName
			msg["activityName"]=self.activityName
			
			# msg=self._urlencode(msg)
		return json.dumps(msg)


if __name__=='__main__':
	def run():
		for i in range(1):
			IP="192.168.130.63"
			PORT="80"
			username="pov%03d"%(i+1) #%03d不足三位数左边补位0
			filename="2016042101.jpg"
			activityName="activityName"+str(i)
			file={"file":open("D:\\_svn\\AiTest\\debug\\resource\\2016042101.jpg","rb")}
			c=client(IP,PORT,username,filename,file,activityName)
			c.main()
			file["file"].close()
	t=threading.Thread(target=run())
	t.setDaemon(True)
	t.start