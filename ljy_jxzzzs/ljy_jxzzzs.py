#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

import ljy_base,ljy_config
import os,sys,time
import traceback
import threading
import json
import random

class common():
	def __init__(self,runtimes,username=None,passwd=None,start_time=None):
		self.conf=ljy_config.getconf().get_config()
		self.cookies={}
		self.runtimes=int(runtimes)
		self.username=""
		if username is not None:
			self.username=username
		self.passwd=passwd
		self.host=self.conf["host"]
		self.index=self.conf["index"]
		self.token=""
		self.userId=""
		self.idCardNo=""
		self.registrationNo=""
		self.loginMobile=""
		self.guardianmobile=int(self.conf["guardianmobile"])+self.runtimes
		# self.guardianmobile=""
		self.realName=""
		self.schoolname=""
		self.Majorinfo={}
		self.Majorinfo_2={}
		self.start_time=start_time

		self.headers={
		"Accept":"application/json, text/plain, */*",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
		"Content-Type":"application/json;charset=UTF-8",
		"Accept-Encoding":"gzip, deflate",
		"Tenant-Id": "E000001",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Origin": "%s"%(self.index),
		"X-User-Uid":"",
		"X-User-Account":""
		}

	def getVerificationCode(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/login/getVerificationCode"
		uri=host+conf["getverificationcode"]
		headers=self.headers
		data={}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		return result["responseEntity"]["code"]

	def sendValidateCode(self,data=None):
		conf=self.conf
		host=self.host
		uri=host+conf["sendvalidatecode"]
		headers=self.headers
		if data is None or data=='':
			data={}
		else:
			data=data
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		return result["responseEntity"]

	def getuserlist(self):
		return ljy_config.getconf().getuserlist()

	def login(self,code):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/login/tologin"
		uri=host+conf["login"]
		headers=self.headers
		username=self.username
		if self.username is None or self.username=='':
			username=self.getuserlist()[self.runtimes]
			self.username=username
		data={
		"c":code,
		"n":username,
		"p":self.passwd,
		"v":""
		}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			self.token=result["responseEntity"]["token"]
			self.userId=result["responseEntity"]["userId"]
			self.idCardNo=result["responseEntity"]["idCardNo"]
			self.registrationNo=result["responseEntity"]["registrationNo"]
			self.realName=result["responseEntity"]["realName"]
			self.loginMobile=result["responseEntity"]["loginMobile"]
			self.loginMobile=self.guardianmobile
			# self.guardianmobile=self.loginMobile
			self.headers["X-User-Uid"]=self.token
			self.headers["X-User-Account"]=self.userId
			#print(self.userId,">",username)
		except Exception:
			print("error；error；error；error；error；error；error；error；%s:登录失败<%s>"%(username,result["serverResult"]["resultMessage"]))
		return result

	def getGraduateschoolList(self):
		conf=self.conf
		host=self.host
		uri=host+conf["getgraduateschoollist"]
		headers=self.headers
		data={"params":{}}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		graduateschoolId=self.getgraduateschoolId()
		for i in result["pageInfo"]["list"]:
			# if i["graduateschoolName"]==schoolname:
			if i["graduateschoolId"]==graduateschoolId:
				self.schoolname=i["graduateschoolName"]
				return i["graduateschoolId"]
				break

	def doUpdatePwd(self,login_result):
		if login_result["serverResult"]["resultCode"]=="201":#201首次登录，200非首次
			conf=self.conf
			host=self.host
			uri=host+conf["doupdatepwd"]
			headers=self.headers
			sendphone={"to":self.guardianmobile}
			code_uuid=self.sendValidateCode(sendphone)
			graduateschoolId=self.getGraduateschoolList()
			ValidateCode=self.getMobileMSG()
			data={"c":"%s"%(code_uuid),#发送手机验证码返回的uuid
				"cp":"%s"%(conf["updatepwd"]),#确认密码
				"graduateschool":"%s"%(graduateschoolId),#初中学校
				"idcardno":"%s"%(self.idCardNo),#身份证
				"p":"%s"%(conf["updatepwd"]),#密码
				"studentname":"%s"%(self.realName),#学生姓名
				"tel":self.guardianmobile,#监护人手机号
				"tno":"%s"%(self.username),
				"userid":"%s"%(self.userId),
				"v":"%s"%(ValidateCode)}#手机验证码
			result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
			result=ljy_base.base().ResultTextConvert(result)
			print(result["serverResult"]["resultMessage"],result["serverResult"]["internalMessage"],">doUpdatePwd(%s)"%(self.username))
		else:
			pass

	def updateBasicInfo(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/updateBasicInfo"
		uri=host+conf["updatebasicinfo"]
		headers=self.headers
		data={"area":"null",
		"className":"%s"%(conf["classname"]),#班级
		"guardianName":"%s%s"%(conf["guardianname"],self.runtimes),#监护人姓名
		"guardianMobile":"%s"%(self.guardianmobile),#监护人联系方式
		"address":"%s"%(conf["address"]),#家庭住址
		"idcardNo":"%s"%(self.idCardNo),#idCardNo
		"registrationNo":"%s"%(self.registrationNo),#报考序号registrationNo
		"schoolName":"%s"%(self.schoolname),#初中学校
		"studentNo":"%s"%(int(conf["studentno"])+self.runtimes),#注册学籍号
		"examNo":"%s"%(self.username),#username
		"studentName":"%s"%(self.realName),#realName
		"editable":"true"}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		print(result["serverResult"]["resultMessage"],">updateBasicInfo(%s)"%(self.username))
		return result

	def getMajorList(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/getMajorList?"
		uri=host+conf["getmajorlist"]
		headers=self.headers
		data={"searchStr":"","batch":"%s"%(conf["batch"]),"numPerPage":1,"pageSize":100}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			return result["responseEntity"]["list"]
		except:
			print(result)

	def getMajorinfo(self,*args):
		volunteerCode=args[0]
		if len(args)>1:
			volunteerCode_2=args[1]
		else:
			volunteerCode_2=""
		MajorList=self.getMajorList()
		if volunteerCode is None or volunteerCode=="":
			choose_id=random.randint(0,len(MajorList)-1)
			self.Majorinfo=MajorList[choose_id]
		else:
			for i in MajorList:
				if i["volunteerCode"]==volunteerCode:
					self.Majorinfo=i
					break
				elif MajorList.index(i)==len(MajorList)-1 and i["volunteerCode"]!=volunteerCode:
					print("error；error；error；error；error；error；error；error；volunteerCode '%s' not found,change to random Mode!"%(volunteerCode))
					self.getMajorinfo()
			for i in MajorList:
				if volunteerCode_2 is not None and volunteerCode_2!="":
					if i["volunteerCode"]==volunteerCode_2:
						self.Majorinfo_2=i
						break

	def getVolunteerInfo(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/getVolunteerInfo"
		uri=host+conf["getvolunteerinfo"]
		headers=self.headers
		params={"batch":int(conf["batch"]),"userId":""}
		params=ljy_base.base()._urlencode(params)
		result=ljy_base.base().getHTTP(uri,params=params,headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		return result["responseEntity"]

	def getgraduateschoolId(self):
		import ljy_ConnDB
		conn=ljy_ConnDB.e000001()
		graduateschoolId=ljy_ConnDB.ConnectDB(conn,self.username)
		graduateschoolId=graduateschoolId.t_jx_user_logininfo()
		# print(graduateschoolId)
		return graduateschoolId

	def getMobileMSG(self):
		import ljy_ConnDB
		conn=ljy_ConnDB.twpaasDB()
		MSGcode=ljy_ConnDB.ConnectDB(conn,self.loginMobile)
		# MSGcode=ljy_ConnDB.ConnectDB(conn,self.guardianmobile)
		MSGcode=MSGcode.t_e_msg_history()
		#print(MSGcode)
		return MSGcode

	def sendMobileValidityCode(self,data=None):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/getValidateCode"
		uri=host+conf["getvalidatecode"]
		headers=self.headers
		if data is None or data=='':
			data={}
		else:
			data=data
		now_time=time.time()
		#防止数据库验证码时间不同，导致排序不稳定
		if abs(now_time-self.start_time)>1.0:
			pass
		else:
			# print(abs(now_time-self.start_time))
			# print("wait 0.5s")
			time.sleep(0.5)
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		if result["serverResult"]["resultMessage"]=="发送成功":
			return result
		else:
			print("%s>getValidateCode(%s)"%(result["serverResult"]["resultMessage"],self.username))

	def saveMajor(self):
		conf=self.conf 
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/"
		uri=host+conf["savemajor"]
		headers=self.headers
		volunteerCode=self.Majorinfo["volunteerCode"]
		data={"userId":"",
		"status":0,#0：保存草稿；1：提交；2：确认
		"volunteerDetailVOList":[{"volunteerCode":"%s"%(volunteerCode),"orderNo":1}],#orderNo第几志愿
		"volunteerApplyList":[{"volunteerCode":"%s"%(volunteerCode),"orderNo":1}],
		"batch":"%s"%(conf["batch"])}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		print(result["serverResult"]["resultMessage"],">saveMajor(%s)"%(self.username))
		return result

	def reportMajor(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/"
		uri=host+conf["reportmajor"]
		headers=self.headers
		VolunteerInfo=self.getVolunteerInfo()
		data=VolunteerInfo
		orderNo={"orderNo":1}
		self.Majorinfo.update(orderNo)
		data["volunteerDetailVOList"]=[self.Majorinfo]
		data_add={"volunteerApplyList":[self.Majorinfo]}
		data.update(data_add)
		if self.Majorinfo_2 is not None and self.Majorinfo_2 != "" and self.Majorinfo_2 != {}:
			orderNo={"orderNo":2}
			self.Majorinfo_2.update(orderNo)
			data["volunteerDetailVOList"].append(self.Majorinfo_2)
			data["volunteerApplyList"].append(self.Majorinfo_2)
		# print(data)
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		print(result["serverResult"]["resultMessage"],">reportMajor(%s)"%(self.username))
		return result

	def checkValidateCode(self):
		self.sendMobileValidityCode()
		MobileMSG=self.getMobileMSG()
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/volunteer/checkValidateCode"
		uri=host+conf["checkvalidatecode"]
		headers=self.headers
		data={"validateCode":"%s"%(MobileMSG),"batch":"%s"%(conf["batch"])}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		print(result["serverResult"]["resultMessage"],">checkValidateCode(%s)"%(self.username))
		return result

	def addstu(self):
		conf=self.conf
		host=self.host
		# uri=host+"/openapi-vocationalenroll/student/add"
		uri=host+conf["addstu"]
		headers=self.headers
		data={"userId":"",
		"realName":"qwe",
		"orgId":"00001",
		"examNo":"",
		"idCardNo":"432522200203020001",
		"chinese":0,
		"math":0,
		"english":0,
		"science":0,
		"sociology":0,
		"sport":0,
		"experiment":0,
		"comprehensive":0,
		"feature":0,
		"total":0,
		"status":"",
		"userType":"1",
		"studentType":"0",
		"registrationNo":"20000000"}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		return result

	def Upload_MultipartFormData(self,file_path):
		conf=self.conf
		host=self.host
		uri=host+"/twasp/fs/fs/file/upload"
		uri=host+conf["upload"]
		file_path=file_path
		headers=self.headers
		headers.pop("Content-Type")
		data={"branchCode":"E000001"}
		#提交files表单固定格式,open(...)部分不能用变量代替：file ={'row_name':(filename,open(file_path,"rb"),'image/jpeg'<-RecContentType)}
		file ={'file':(file_path.split("\\")[-1],open(file_path,"rb"),'application/vnd.ms-excel')}
		# file ={'file':(conf["filename"],open(".\\zero.jpg","rb"),'image/jpeg')}
		result=ljy_base.base().postHTTP(uri,data=data,files=file,headers=headers)
		result=ljy_base.base().ResultTextConvert(result)
		# ljy_base.base().showResult(result)
		file["file"][1].close()
		return result
		#print(result)

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
		code=self.getVerificationCode()
		login_result=self.login(code)
		if conf["custommethod"]=="True":
			self.CustomMethod(httpMethod=conf["httpmethod"],params=conf["params"],uri=conf["uri"],data=conf["data"],headers_add=conf["headers_add"],cookies=conf["cookies"])
		else:
			self.doUpdatePwd(login_result)
			self.updateBasicInfo()
			self.getMajorinfo(conf["volunteercode"],conf["volunteercode_2"])
			self.saveMajor()
			self.reportMajor()
			self.checkValidateCode()
			#self.logout()
			#self.addstu()
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