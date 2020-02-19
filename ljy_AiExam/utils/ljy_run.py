'''
 * @Author: lijiayi 
 * @Date: 2019-06-28 11:57:17 
 * @Last Modified by: lijiayi
 * @Last Modified time: 2019-06-28 13:45:54
 '''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

from utils import ljy_base,ljy_config
import os,sys,time
import traceback
import threading
import json
import random

# try:
# 	os.chdir(os.path.dirname(sys.argv[0]))
# except:
# 	pass

class common():
	def __init__(self,runtimes,username=None,passwd=None,start_time=None,studentIdList=None):
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
		self.token=self.conf["token"]
		self.userId=""
		#headers
		self.cookies={}
		self.headers={
		"Accept":"application/json, text/plain, */*",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
		"Content-Type":"application/json;charset=UTF-8",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Access-Token":self.token,
		"Tenant-Id":self.conf["tenant-id"],
		"Origin": "%s"%(self.host)
		}
		self.publishId=""
		self.paperId=""#试卷ID
		self.examId=""#考试ID
		self.classId=""
		self.studentId_first=""#第一个手动上传作答图片的学生
		self.studentIdlist=[]
		self.studentId=""#userid
		self.examNumber=0#考号
		self.subjectId=""
		self.schoolId=self.conf["schoolid"]
		self.examinfo=[]

	def studentIdList(self):
		self.studentIdlist=ljy_config.getconf().getstudentIdlist()
		return ljy_config.getconf().getstudentIdlist()

	#get exam_list
	def getExamList(self):
		conf=self.conf
		host=self.host
		uri=host+conf["c_getexamlist"]
		headers=self.headers
		headers["Content-Type"]="application/json; charset=UTF-8"
		data={"orgId":"%s"%(self.schoolId)}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		return result
	
	#get examId
	def getexamId(self):
		conf=self.conf
		getExamList=self.getExamList()
		try:
			examlist=getExamList["pageInfo"]["list"]
		except:
			ex=Exception(getExamList)
			raise ex
		examname=conf["upload_examname"]
		for i in examlist:
			if i["examName"]==examname:
				self.examId=i["examId"]
				self.examinfo=i
				# self.publishId=i["gradeList"][0]["subjectList"][0]["publishId"]
				# print("examId:%s"%(self.examId))
				break
			elif examlist.index(i)==len(examlist)-1 and i["upload_examname"]!=examname:
				ex=Exception("error；error；error；error；error；error；error；error；Exam '%s' not found!"%(examname))
				raise ex

	#get paperId subjectId
	def getScanInfo(self):
		conf=self.conf
		host=self.host
		uri=host+conf["c_getscaninfo"]
		headers=self.headers
		headers["Content-Type"]="application/json; charset=UTF-8"
		data={"examId":"%s"%(self.examId),"orgId":"%s"%(self.schoolId)}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		subjectName=conf["subjectname"]
		try:
			if subjectName != "" or subjectName is not None:
				for i in result["pageInfo"]["list"]:
					if subjectName==i["subjectName"]:
						self.subjectId=i["subjectId"]
						self.paperId=i["paperId"]
						break
			else:
				self.subjectId=result["pageInfo"]["list"][0]["subjectId"]
				self.paperId=result["pageInfo"]["list"][0]["paperId"]
			# print("paperId:%s,subjectId:%s"%(self.paperId,self.subjectId))
		except:
			ex=Exception(result)
			raise ex
		self.getpublishId()
		return result

	#get publishId
	def getpublishId(self):
		gradeId=self.conf["gradeid"]
		subjectList=[]
		for i in self.examinfo["gradeList"]:
			if i["gradeId"] == gradeId:
				subjectList=i["subjectList"]
				for x in subjectList:
					if self.subjectId==x["subjectId"]:
						self.publishId=x["publishId"]
						break
				break


	#get examNumber,classId
	def getStudentList(self):
		conf=self.conf
		host=self.host
		uri=host+conf["c_getstudentlist"]
		headers=self.headers
		headers["Content-Type"]="application/json; charset=UTF-8"
		data={"examId":"%s"%(self.examId),"gradeId":"%s"%(conf["gradeid"])}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			classList=result["pageInfo"]["list"]
		except:
			ex=Exception("列表空，确认年级id是否正确，list is Null,check conf[gradeid]\n %s"%(result))
			raise ex
		for i in classList:
			StudentList=i["students"].split("#")
			for x in StudentList:
				if self.studentId == x.split(",")[1]:
					self.examNumber=x.split(",")[0]
					self.classId=i["classId"]
					break
				# elif classList.index(i) == len(classList)-1 and StudentList.index(x) == len(StudentList)-1 and self.studentId != x.split(",")[1]:
				# 	ex=Exception("学生id:%s在当前考试未找到，student not found in this exam,check conf"%(self.studentId))
				# 	raise ex
		if self.classId =="" or self.classId is None:
			ex=Exception("'%s' Not Found in this exam!\n%s"%(self.studentId,classList))
			raise ex

	def getExamInfo_init(self):
		self.getexamId()#get examId
		self.getScanInfo()#get paperId subjectId

	def get_QandA_answerinfo(self):
		answer={
			"answerList": [{
				#aiexam/2019/7/19/zip/answerSheet/examId/paperId/studentId/071914264585/questionId_0.jpg
				"answerPath": "",
				"userAnswer": None,
				"sequenceNo": "0",
				"abnormal": None,
				"result": None,
				"score": None,
				"markPath": None
				}],
				"childId": None,
				"questionId": "",
				"defaultScore": 0.0,
				"typeLevel": "4",
				"questionLable": None,
				"rowLable": None,
				"itemCount": None,
				"questionTop": 740,
				"questionLeft": 984,
				"pageNumber": 1
				}
		return answer

	def get_questionList_info(self):
		conf=self.conf	
		data=[]
		questionIdList=conf["questionidlist"].split(",")
		typeLevel=conf["typelevel"].split(",")#4填空题，5简答题
		for i in range(len(questionIdList)):
			answer=self.get_QandA_answerinfo()#赋值放在for里面，防止改变原dict值,a=1,b=a,b=2,a==2 is True
			answerPath_temp=conf["snapshot"].split("/")
			if int(typeLevel[i])<4:
				answerPath_temp[-1]="group_1.jpg"
			else:
				answerPath_temp[-1]="%s_0.jpg"%(questionIdList[i])
			answerPath='/'
			answerPath=answerPath.join(answerPath_temp)
			answer["answerList"][0]["answerPath"]=answerPath
			answer["questionId"]=questionIdList[i]
			# top_left=conf["top_left"]
			top_left="924/985"
			answer["top"],answer["left"]=int(top_left.split("/")[0]),int(top_left.split("/")[1])
			answer["typeLevel"]=typeLevel[i]
			data.append(answer)
		return data


	def get_saveStuAnswer_info(self):
		self.getExamInfo_init()
		conf=self.conf
		studentIdlist=[]
		studentIdlist=self.studentIdlist
		self.studentId_first=studentIdlist[0]
		self.studentId=studentIdlist[self.runtimes]
		self.getStudentList()
		abnormalReason=conf["abnormalreason"]
		if abnormalReason is None or abnormalReason == "":
			abnormalReason="successful"
		data={
			"abnormalReason": "%s"%(abnormalReason),
			"paperId": "%s"%(self.paperId),
			"examId": "%s"%(self.examId),
			"orgId": "%s"%(self.schoolId),
			"classId": "%s"%(self.classId),
			"publishId": "%s"%(self.publishId),
			"abnormal": "0",
			"absent": "0",#缺考
			"paperAnswer": {
				"snapshot": "%s"%(conf["snapshot"]),
				"questionList": [],
				"objectiveLeft": "0",
				"objectiveTop": "0",
				"totalLeft": "%s"%(conf["totalleft"]),
				"totalTop": "%s"%(conf["totaltop"])
			},
			"studentId": "%s"%(self.studentId),
			"examNumber": "%s"%(self.examNumber),
			"subjectId": "%s"%(self.subjectId),
			"abnormalId": None,#异常ID
			"abnormalType": None,
			"hasSubjectives": "1",
			"markType": "0",
			"cover": None
			}
		if abnormalReason == "缺考":
			data["absent"]="1"
		if conf["snapshot_2"] is not None or conf["snapshot_2"] != "":
			data["paperAnswer"]["answerSheetSnapshot"]=conf["snapshot"]+";"+conf["snapshot_2"]
		questionList_info=self.get_questionList_info()#题目作答列表
		data["paperAnswer"]["questionList"]=questionList_info
		#examNumber=questionList_info[0]["answerList"][0]["answerPath"].split("/")[-2]
		return data
		
	def saveStudentAnswer(self):
		# self.paperId,self.examId,self.studentId_first,self.studentId,self.subjectId
		conf=self.conf
		host=self.host
		uri=host+conf["c_savestudentanswer"]
		headers=self.headers
		headers["Content-Type"]="application/json; charset=UTF-8"
		data=self.get_saveStuAnswer_info()
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
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
		# login_result=self.login()
		if conf["custommethod"]=="True":
			self.CustomMethod(httpMethod=conf["httpmethod"],params=conf["params"],uri=conf["uri"],data=conf["data"],headers_add=conf["headers_add"],cookies=conf["cookies"])
		else:
			# self.getExamList()
			result=self.saveStudentAnswer()
			#self.logout()
			# file_path="C:\\Users\\povti\\Downloads\\导入学生帐号.xls"
			# self.Upload_MultipartFormData(file_path)
		stop_time=time.time()
		print("(%s)总共耗时:{0:.5f}秒>>执行结果(%s)".format(stop_time-self.start_time)%(self.studentId,result))


if __name__ == '__main__':
	c=ljy_config.getconf().get_config()
	try:
		for i in range(int(c["loop"])):
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

