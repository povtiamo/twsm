'''
 * @Author: lijiayi 
 * @Date: 2019-06-28 11:57:17 
 * @Last Modified by: lijiayi
 * @Last Modified time: 2019-06-28 13:45:54
 '''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7



import ljy_base,ljy_config
import os,sys,time
import traceback
import threading
import json
import random

try:
	os.chdir(os.path.dirname(sys.argv[0]))
except:
	pass

class common():
	def __init__(self,runtimes,username=None,passwd=None,start_time=None):
		#conf
		self.conf=ljy_config.getconf().get_config()
		self.host=self.conf["host"]
		self.runtimes=int(runtimes)
		#info
		self.start_time=start_time
		self.username=""
		if username is not None:
			self.username=username
		self.passwd=passwd
		self.token=""
		self.userId=""
		#headers
		self.cookies={}
		self.headers={
		"Accept":"application/json, text/plain, */*",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
		"Content-Type":"application/json;charset=UTF-8",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Origin": "%s"%(self.host)
		}
		self.examname=self.conf["examname"]
		self.paperId=""
		self.examPlanId=""
		self.examSubject=""
		self.paperStatusId="" 
		self.questionId_1=self.conf["questionid1"]
		self.questionId_2=self.conf["questionid2"]
		


	def checkLoginName(self):
		conf=self.conf
		host=self.host
		uri=host+conf["checkloginname"]
		headers=self.headers
		headers["Content-Type"]="application/x-www-form-urlencoded; charset=UTF-8"
		params={"_":ljy_base.base().timeStamp()}
		data={"loginName":self.username}
		data=ljy_base.base()._urlencode(data)
		result=ljy_base.base().postHTTP(uri,params=params,data=data,headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		return result

	def getuserlist(self):
		return ljy_config.getconf().getuserlist()

	def getcookies(self):
		uri=self.host+self.conf["index"]
		result=ljy_base.base().getHTTP(uri)
		self.cookies={"JSESSIONID":"%s"%(result.cookies["JSESSIONID"])}

	def getloginId(self):
		loginId={"username":self.username,"password":self.conf["passwd"]}
		loginId=ljy_base.base()._urlencode(loginId)
		return ljy_base.base().To_Base64(loginId)

	def login(self):
		conf=self.conf
		host=self.host
		uri=host+conf["login"]
		headers=self.headers
		headers["Content-Type"]="application/x-www-form-urlencoded; charset=UTF-8"
		username=self.username
		if self.username is None or self.username=='':
			username=self.getuserlist()[self.runtimes]
			self.username=username
		params={"_":ljy_base.base().timeStamp()}
		loginId=self.getloginId()
		data={"loginId":"%s"%(loginId),
		"applicationId":"",
		"rememberPwd":True}
		data=ljy_base.base()._urlencode(data)
		result=ljy_base.base().postHTTP(uri,params=params,data=data,headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			self.userId=result["userLoginInfo"]["userId"]
			# print(self.userId,">",username)
		except Exception:
			ex=Exception("error；error；error；error；error；error；error；error；'%s':登录失败<%s>"%(username,result["serverResult"]["resultMessage"]))
			raise ex
		return result

	def addClass(self):
		pass

	def addTeacher(self):
		pass
	
	def addStudent(self):
		pass
	
	def SetAccess(self):
		pass

	def SetCharacter(self):
		pass
	
	def SetClassSub(self):
		pass
	

	def CustomMethod(self,httpMethod,uri,params=None,data=None,headers_add=None,cookies=None):
		# import pdb
		# pdb.set_trace()
		# print(uri,params,data,headers_add,cookies)
		headers=self.headers
		if params is not None:
			try:
				params=json.loads(params)
			except:
				pass
			params=ljy_base.base()._urlencode(params)
		else:
			params=None
		if data is not None:
			data=data
		else:
			data=""
		if headers_add is not None:
			try:
				headers.update(json.loads(headers_add))
			except:
				pass
		else:
			pass
		if cookies is not None:
			try:
				cookies=json.loads(cookies)
			except:
				pass
		else:
			pass
		if httpMethod=="get":
			result=ljy_base.base().getHTTP(uri,params=params,headers=headers,cookies=cookies)
		else:
			result=ljy_base.base().postHTTP(uri,params=params,data=data,headers=headers,cookies=cookies)
		result=ljy_base.base().ResultTextConvert(result)
		print(result)

	def logout(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/login/logout"
		uri=host+conf["logout"]
		headers=self.headers
		result=ljy_base.base().getHTTP(uri,headers=headers)
		return result.headers


	def main(self):
		conf=self.conf
		self.getcookies()
		self.checkLoginName()
		login_result=self.login()
		if conf["custommethod"]=="True":
			self.CustomMethod(httpMethod=conf["httpmethod"],params=conf["params"],uri=conf["uri"],data=conf["data"],headers_add=conf["headers_add"],cookies=conf["cookies"])
		else:
			pass
			#self.logout()
			# file_path="C:\\Users\\povti\\Downloads\\导入学生帐号.xls"
			# self.Upload_MultipartFormData(file_path)
		stop_time=time.time()
		print("(%s)总共耗时:{0:.5f}秒".format(stop_time-self.start_time)%(self.username))


if __name__ == '__main__':
	c=ljy_config.getconf().get_config()
	try:
		for i in range(int(c["loop"])):
		# for i in range(2000):
			# passwd="dxk689kxb9j4OUEe7NHVRQ%3D%3D"
			passwd=c["passwd"]
			username=""
			start_time=time.time()
			a=common(i,username,passwd,start_time)
			target=threading.Thread(target=a.main)	#这里的函数不要加()
			#threading.active_count()线程数量,手动限制每次开启的线程数量
			while threading.active_count()>500:
				time.sleep(10)
			target.start()
			#threading.Thread.__stop()

	except KeyboardInterrupt:
		print("key break!")
		sys.exit()