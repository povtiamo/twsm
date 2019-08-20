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
		self.__version=self.conf["version"]
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
		if self.__version=="C04":
			data={"loginId":"%s"%(self.username),"staticmm":"123456","applicationId":"","rememberPwd":True}
		else:
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

	def saveQuestion_single(self):
		conf=self.conf
		uri=conf["host"]+conf["savequestion"]
		headers=self.headers
		headers["Content-Type"]="application/json;charset=UTF-8"
		for i in range(10):
			data={"title":"<div>纯客观题-单选题%s</div><span></span>"%(i+6),"note":"123<br>","answerList":[{"content":0,"sequenceNo":0}],"items":[{"sequenceNo":0,"content":"<p>a</p>"},{"sequenceNo":1,"content":"<p>b</p>"},{"sequenceNo":2,"content":"<p>c</p>"},{"sequenceNo":3,"content":"<p>d</p>"}],"rowlable":1,"typeLevel":"1","labelId":"1","defaultScore":"2","gradeName":"1","subjectName":"100000000007","paragraphId":"PRIMARY_SCHOOL","degree":"1","knowledge":["CNBJTW0100000001118"],"fileList":[],"noteFileList":[],"questionType":"0"}
			result=ljy_base.base().postHTTP(uri,data=json.dumps(data).replace(" ",""),headers=headers,cookies=self.cookies)
			result=ljy_base.base().ResultTextConvert(result)
		# print(result)
	
	def saveQuestion_multiple(self):
		conf=self.conf
		uri=conf["host"]+conf["savequestion"]
		headers=self.headers
		headers["Content-Type"]="application/json;charset=UTF-8"
		subjectName="100000000001"
		paragraphId="PRIMARY_SCHOOL"
		knowledge="CNBJTW0600000020005"
		for i in range(10):
			data={
				"title":"数据建造——填空题%02d【_】【_】【_】"%(i),
				"note":"123",
				"answerList":[
					{"content":"<p>1</p>","sequenceNo":0},
					{"content":"<p>2</p>","sequenceNo":1},
					{"content":"<p>3</p>","sequenceNo":2}
					],
				"isAutoMark":0,
				"typeLevel":"4",
				"labelId":"4",
				"defaultScore":"3",
				"gradeName":"10",
				"subjectName":"%s"%(subjectName),
				"paragraphId":"%s"%(paragraphId),
				"degree":"1",
				"knowledge":["%s"%(knowledge)],
				"fileList":[],
				"noteFileList":[],
				"questionType":"0"}
			data={
				"title":"数据建造——简答题%02d"%(i),
				"note":"123",
				"answerList":[{"content":"<p>123</p>","sequenceNo":0}],
				"typeLevel":"5",
				"labelId":"6",
				"defaultScore":"5",
				"gradeName":"10",
				"subjectName":"%s"%(subjectName),
				"paragraphId":"%s"%(paragraphId),
				"degree":"1",
				"knowledge":["%s"%(knowledge)],
				"fileList":[],
				"noteFileList":[],
				"questionType":"0"}
			result=ljy_base.base().postHTTP(uri,data=json.dumps(data).replace(" ",""),headers=headers,cookies=self.cookies)
			result=ljy_base.base().ResultTextConvert(result)

	def saveQuestion_QandA(self):
		conf=self.conf
		uri=conf["host"]+conf["savequestion"]
		headers=self.headers
		headers["Content-Type"]="application/json;charset=UTF-8"
		for i in range(30):
			data={"title":"数据建造—简答题%s<br>"%(i+30),"note":"123<br>","answerList":[{"content":"<p>123</p>","sequenceNo":0}],"typeLevel":"5","labelId":"6","defaultScore":"5","gradeName":"1","subjectName":"100000000007","paragraphId":"PRIMARY_SCHOOL","degree":"1","knowledge":["CNBJTW0100000001118"],"fileList":[],"noteFileList":[],"questionType":"0"}
			result=ljy_base.base().postHTTP(uri,data=json.dumps(data).replace(" ",""),headers=headers,cookies=self.cookies)
			result=ljy_base.base().ResultTextConvert(result)

	#get paperId examPlanId examSubject
	def queryExamInfoForPage(self):
		conf=self.conf
		uri=conf["host"]+conf["queryexaminfoforpage"]
		headers=self.headers
		headers["Content-Type"]="application/x-www-form-urlencoded; charset=UTF-8"
		params={"_":ljy_base.base().timeStamp()}
		data={
		"pageNo":1,
		"pageSize":4,
		"examPlanName":"%s"%(self.examname)
		}
		data=ljy_base.base()._urlencode(data)
		result=ljy_base.base().postHTTP(uri,params=params,data=data,headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			result=result["result"]["resultList"][0]
		except:
			ex=Exception("queryExamInfoForPage>>>%s"%(result))
			raise ex
		self.paperId=result["paperId"]
		self.examPlanId=result["examPlanId"]
		self.examSubject=result["examSubjectId"]
		return result
		
	#get paperStatusId
	def examstart(self):
		conf=self.conf
		uri=conf["host"]+conf["examstart"]
		headers=self.headers
		headers["Content-Type"]="application/x-www-form-urlencoded; charset=UTF-8"
		# headers_add={"Referer": "%s/examination/paper/exercise?paperId=%s"%(conf["host"],self.paperId)}
		# headers.update(headers_add)
		data={
			"paperId":"%s"%(self.paperId),
			"examPlanId":"%s"%(self.examPlanId),
			"examSubject":"%s"%(self.examSubject)
		}
		data=ljy_base.base()._urlencode(data)
		result=ljy_base.base().postHTTP(uri,data=data,headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			self.paperStatusId=result["paperStatusId"]
		except:
			if conf["paperstatusid_temp"]=="" or conf["paperstatusid_temp"] is None:
				ex=Exception("paperStatusId False!>>>%s"%(result))
				raise ex
			else:
				self.paperStatusId=conf["paperstatusid_temp"]
		return result

	def checkExamEnd(self):
		conf=self.conf
		uri=conf["host"]+conf["checkexamend"]
		headers=self.headers
		headers["Content-Type"]="application/x-www-form-urlencoded; charset=UTF-8"
		# headers_add={"Referer": "%s/examination/paper/exercise?paperId=%s"%(conf["host"],self.paperId)}
		# headers.update(headers_add)
		data={
			"examPlanId":"%s"%(self.examPlanId),
			"examGrade":"1",
			"examSubject":"%s"%(self.examSubject)
		}
		data=ljy_base.base()._urlencode(data)
		result=ljy_base.base().postHTTP(uri,data=data,headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		# print(result)

	def Init_Stu_ExamInfo(self):
		self.queryExamInfoForPage()
		self.examstart()
		self.checkExamEnd()
		if self.paperStatusId=="" or self.paperStatusId==None:
			print("%s get paperStatusId False!"%(self.username))

	def Get_saveAnswerBlank_info(self):
		data={
			"examPlanId": "%s"%(self.examPlanId),
			"paperResults": [{
				"paperId": self.paperId,
				"examPlanId": self.examPlanId,
				"examSubject": self.examSubject,
				"userAnswer": "",#选择题(0A/1B/2C/3D)和简答题回答
				"useTime": "10",
				"fileList": [],
				"paperStatusId": self.paperStatusId,
				"questionId":"0",
				"typeLevel": "0",#1单选题、2多选题、3判断题、4填空题、5简答题
				"typeLevelLabelId": "0",#1单选题、2多选题、3判断题、4填空题、6简答题
				"markStatus": "0",
				"score": 3,
				"answers": []#填空类回答
				}]
			}
		if self.__version=="C04":
			data.pop("examPlanId")
		else:
			pass
		return data

	def Get_saveAnswerOther_info(self):
		data={
			"examPlanId": "%s"%(self.examPlanId),
			"paperResults": [{
				"paperId": self.paperId,
				"examPlanId": self.examPlanId,
				"examSubject": self.examSubject,
				"userAnswer": "0",
				"useTime": "10",
				"fileList": [],
				"paperStatusId": self.paperStatusId,
				"questionId":"0",
				"typeLevel": "0",
				"typeLevelLabelId": "0",
				"markStatus": "0"}]
			}
		if self.__version=="C04":
			data.pop("examPlanId")
		else:
			pass
		return data

	def saveAnswer(self):
		conf=self.conf
		headers=self.headers
		headers["Content-Type"]="application/json"
		# headers_add={"Referer": "%s/examination/paper/exercise?paperId=%s"%(conf["host"],self.paperId)}
		# headers.update(headers_add)
		questionidlist=conf["r_questionidlist"].split(",")
		typeLevellist=conf["r_typelevel"].split(",")
		answerlist=conf["answerlist"].split(",")
		typeLevelLabelId=0
		params=None
		data={}
		uri=""
		for i in range(len(questionidlist)):
			typeLevelLabelId=typeLevellist[i]
			if i<int(len(questionidlist))-1:
				uri=conf["host"]+conf["saveanswer"]
			else:
				uri=conf["host"]+conf["submitpaper"]
				params={"paperStatusId":self.paperStatusId}
			if int(typeLevellist[i])==4:#填空题
				data=self.Get_saveAnswerBlank_info()
				answers=[]
				sequencelist=answerlist[i].split("/")
				for x in range(len(sequencelist)):
					answer={"sequenceNo":int(x),"userAnswer":"%s"%(sequencelist[x])}
					answers.append(answer)
				data["paperResults"][0]["answers"]=answers
			else:
				if int(typeLevellist[i])==5:
					typeLevelLabelId=6
				data=self.Get_saveAnswerOther_info()
				data["paperResults"][0]["userAnswer"]=answerlist[i]
			data["paperResults"][0]["questionId"]=questionidlist[i]
			data["paperResults"][0]["typeLevel"]=typeLevellist[i]
			data["paperResults"][0]["typeLevelLabelId"]=typeLevelLabelId
			result=ljy_base.base().postHTTP(uri,params=params,data=json.dumps(data).replace(" ",""),headers=headers,cookies=self.cookies)
			result=ljy_base.base().ResultTextConvert(result)
		try:
			result=result["resultCode"]
		except:
			result=False
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
		cookies=self.cookies
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
				cookies.update(json.loads(cookies))
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
		result=True
		conf=self.conf
		self.getcookies()
		self.checkLoginName()
		self.login()
		if conf["custommethod"]=="True":
			self.CustomMethod(httpMethod=conf["httpmethod"],params=conf["params"],uri=conf["uri"],data=conf["data"],headers_add=conf["headers_add"],cookies=conf["cookies"])
		else:
			# self.saveQuestion_multiple()
			self.Init_Stu_ExamInfo()
			result=self.saveAnswer()
			self.queryExamInfoForPage()
			#self.logout()
			# file_path="C:\\Users\\povti\\Downloads\\导入学生帐号.xls"
			# self.Upload_MultipartFormData(file_path)
		stop_time=time.time()
		print("(%s)总共耗时:{0:.5f}秒>>执行结果(%s)".format(stop_time-self.start_time)%(self.username,result))


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
			while threading.active_count()>int(c["thread"]):
				time.sleep(10)
			target.start()
			#threading.Thread.__stop()

	except KeyboardInterrupt:
		print("key break!")
		sys.exit()

