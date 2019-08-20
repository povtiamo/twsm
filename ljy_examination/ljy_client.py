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
		self.paperId=""#试卷ID
		self.examId=""#考试ID
		self.studentId_first=""#第一个手动上传作答图片的学生
		self.studentIdlist=[]
		self.studentId=""#考号
		self.subjectId=""
		self.schoolId=self.conf["schoolid"]

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
		data={"schoolId":"%s"%(self.schoolId),"isScan":"1"}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		return result
	
	#get examId
	def getexamId(self):
		conf=self.conf
		examlist=self.getExamList()["examList"]
		examname=conf["upload_examname"]
		for i in examlist:
			if i["examName"]==examname:
				self.examId=i["examId"]
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
		data={"examId":"%s"%(self.examId),"schoolId":None}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)
		try:
			self.paperId=result["gradeScanList"][0]["subjectScanInfoList"][0]["paperId"]
			self.subjectId=result["gradeScanList"][0]["subjectScanInfoList"][0]["subjectId"]
			# print("paperId:%s,subjectId:%s"%(self.paperId,self.subjectId))
		except:
			ex=Exception(result)
			raise ex
		return result

	#get 
	def getExamAbnormalDataList(self):
		conf=self.conf
		host=self.host
		uri=host+conf["c_getexamabnormaldaatalist"]
		headers=self.headers
		headers["Content-Type"]="application/json; charset=UTF-8"
		data={"paperId":"%s"%(self.paperId),
			"examId":"%s"%(self.examId),
			"subjectId":"%s"%(self.subjectId),
			"schoolId":"%s"%(self.schoolId)}
		result=ljy_base.base().postHTTP(uri,data=json.dumps(data),headers=headers,cookies=self.cookies)
		result=ljy_base.base().ResultTextConvert(result)

	def getExamInfo_init(self):
		self.getexamId()#get examId
		self.getScanInfo()#get paperId subjectId

	def get_QandA_answerinfo(self):
		answer={
			"answerList": [{
				#aiexam/2019/7/19/zip/answerSheet/examId/paperId/studentId/071914264585/questionId_0.jpg
				"answerPath": "",
				"content": None,
				"sequenceNo": "0",
				"isAbnormal": None,
				"result": None,
				"score": None
				}],
				"childId": None,
				"questionId": "",
				"defaultScore": 0.0,
				"typeLevel": "4",
				"questionLable": None,
				"rowLable": None,
				"itemCount": None,
				"top": 740,
				"left": 984,
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
			top_left=conf["top_left"]
			answer["top"],answer["left"]=int(top_left.split("/")[0]),int(top_left.split("/")[1])
			answer["typeLevel"]=typeLevel[i]
			data.append(answer)
		return data


	def get_saveStuAnswer_info(self):
		self.getExamInfo_init()
		conf=self.conf
		studentIdlist=[]
		studentIdlist=self.studentIdlist
		# print(studentIdlist[0])
		self.studentId_first=studentIdlist[0]
		self.studentId=studentIdlist[self.runtimes]
		data={
			"abnormalReason": "successful",
			"paperId": "%s"%(self.paperId),
			"examId": "%s"%(self.examId),
			"isAbnormalSheet": "0",
			"isAbsentExam": "0",
			"paperAnswer": {
				"answerSheetSnapshot": "%s"%(conf["snapshot"]),
				"questionList": [],
				"objectiveLeft": "0",
				"objectiveTop": "0",
				"totalLeft": "%s"%(conf["totalleft"]),
				"totalTop": "%s"%(conf["totaltop"])
			},
			"studentId": "%s"%(self.studentId),
			"subjectId": "%s"%(self.subjectId),
			"isCover": None,
			"abnormalId": None,#异常ID
			"abnormalType": None,
			"paperStatusId": None}
		if conf["snapshot_2"] is not None or conf["snapshot_2"] != "":
			data["paperAnswer"]["answerSheetSnapshot"]=conf["snapshot"]+";"+conf["snapshot_2"]
		data["paperAnswer"]["questionList"]=self.get_questionList_info()#题目作答列表
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
		# for i in range(2000):
			# passwd="dxk689kxb9j4OUEe7NHVRQ%3D%3D"
			passwd=c["passwd"]
			username=""
			start_time=time.time()
			a=common(i,username,passwd,start_time)
			a.studentIdList()
			target=threading.Thread(target=a.main)	#这里的函数不要加()
			#threading.active_count()线程数量,手动限制每次开启的线程数量
			while threading.active_count()>int(c["thread"]):
				time.sleep(10)
			target.start()
			#threading.Thread.__stop()

	except KeyboardInterrupt:
		print("key break!")
		sys.exit()