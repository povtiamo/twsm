''' 
* @Author: lijiayi  
* @Date: 2019-07-02 15:05:30  
* @Last Modified by:   lijiayi  
* @Last Modified time: 2019-07-02 15:05:30  
'''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

#configparser配置文件key必须小写
import configparser
import os,sys
# import time,datetime
import random


class getconf():
	def __init__(self):
		self._path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.conf = configparser.ConfigParser()
		self.conf.read(self.get_config_path(),encoding="utf-8-sig")
		self.DBconf = configparser.ConfigParser()
		self.DBconf.read(self.get_DB_config_path(),encoding="utf-8-sig")

	def get_config_path(self):
		# _file_path=os.path.dirname(sys.argv[0])+"\\config\\conf.ini"
		_file_path=self._path+"\\config\\conf.ini"
		if os.path.exists(_file_path):
			return _file_path
		else:
			# raise
			print("'%s' not found!"%(_file_path))
			sys.exit()
	
	def get_DB_config_path(self):
		# _file_path=os.path.dirname(sys.argv[0])+"\\config\\conf.ini"
		_file_path=self._path+"\\config\\DBconf.ini"
		if os.path.exists(_file_path):
			return _file_path
		else:
			# raise
			print("'%s' not found!"%(_file_path))
			sys.exit()

	def get_data_path(self):
		# _file_path=os.path.dirname(sys.argv[0])+"\\data\\"
		_file_path=self._path+"\\data\\"
		if os.path.exists(_file_path):
			return _file_path
		else:
			# raise
			print("'%s' not found!"%(_file_path))
			sys.exit()
		
	def get_log_path(self):
		# _file_path=os.path.dirname(sys.argv[0])+"\\data\\"
		_file_path=self._path+"\\log\\"
		if os.path.exists(_file_path):
			return _file_path
		else:
			# raise
			print("'%s' not found!"%(_file_path))
			sys.exit()

	def get_resource_path(self):
		# _file_path=os.path.dirname(sys.argv[0])+"\\resource\\"
		_file_path=self._path+"\\resource\\"
		if os.path.exists(_file_path):
			return _file_path
		else:
			# raise
			print("'%s' not found!"%(_file_path))
			sys.exit()

	def get_config(self):
		conf_dict={}
		try:
			conf_dict.update(dict(self.conf["info"]))
			conf_dict.update(dict(self.conf["path"]))
			conf_dict.update(dict(self.conf["sys"]))
			conf_dict.update(dict(self.conf["client"]))
			conf_dict.update(dict(self.conf["custommethod"]))
		except Exception:
			ex=Exception("读取%s出错，注意格式是否正确，以及%%是否转义;;;read conf.ini error，plz check out"%(self.get_config_path()))
			raise ex
		return conf_dict

	def get_DB_config(self):
		conf_dict={}
		try:
			conf_dict.update(dict(self.DBconf["db"]))
			conf_dict.update(dict(self.DBconf["file"]))
		except Exception:
			ex=Exception("读取%s出错，注意格式是否正确，以及%%是否转义;;;read conf.ini error，plz check out"%(self.get_DB_config_path()))
			raise ex
		return conf_dict

	def get_table_config(self,tablename):
		conf_dict={}
		try:
			conf_dict.update(dict(self.DBconf["%s"%(tablename)]))
		except Exception:
			ex=Exception("读取%s出错，注意格式是否正确，以及%%是否转义;;;read conf.ini error，plz check out"%(self.get_DB_config_path()))
			raise ex
		return conf_dict

	def runtimes(self):
		conf=self.get_config()
		runtimes=conf["runtimes"]
		return runtimes

	def get_imagepath(self):
		conf=self.get_config()
		image=""
		image_path=conf["image_path"]
		imagelist=[]
		for item in os.listdir(image_path):
			isimage=item.split(".")[-1]
			if isimage in (conf["image_type"]):
				imagelist.append(item)
			else:
				# print(isimage)
				pass
		if len(imagelist)>0:
			image=imagelist[random.randint(0,len(imagelist)-1)]
		else:
			print("Error:\nThere was no imagefile>>%s"%(conf["image_path"]))
		full_path=os.path.join(image_path,image)
		return full_path

	def getsqllist(self):
		conf=self.get_DB_config()
		sqlstrlist_file=self.get_data_path()+conf["sqlstr_file"]
		sqlstr_list=[]
		if os.path.exists(sqlstrlist_file):
			with open(sqlstrlist_file,"rb") as f:
				f=f.read().decode('utf-8').replace("\n"," ").replace("\r"," ").replace("\t"," ")
				# print("read>",f)
				try:
					for i in f.split(";"):
						if i not in sqlstr_list and i not in ("","   "," ","  ","     "):
							i=i.strip(" ")
							if i[0]!="#":
								sqlstr_list.append(i+";") 
							else:
								pass
						else:
							pass
					# if sqlstr_list[-1]==";":
					# 	sqlstr_list.pop(-1)
				except Exception as e:
					ex=Exception("SQL格式错误，检查是否漏填';'\n%s"%(e))
					raise ex
		else:
			print("%s not found!"%(sqlstrlist_file))
			return -1
		return sqlstr_list

	def getuserlist(self):
		conf=self.get_config()
		userlist=[]
		userlist_file=self.get_data_path()+conf["userlistfile"]
		if os.path.exists(userlist_file):
			with open(userlist_file,"rb") as f:
				#replace替换文档中的换行
				f=f.read().decode('utf-8').replace("\n","").replace("\r","").replace("\t","").replace("\"","")
				for i in f.split(","):
					if i not in userlist:
						userlist.append(i)
					else:
						pass
			return userlist
		else:
			print("%s not found!"%(userlist_file))
			return -1
		
	def getstudentIdlist(self):
		conf=self.get_config()
		userlist=[]
		userlist_file=self.get_data_path()+conf["studentidfile"]
		if os.path.exists(userlist_file):
			with open(userlist_file,"rb") as f:
				#replace替换文档中的换行
				f=f.read().decode('utf-8').replace("\n","").replace("\r","").replace("\t","").replace("\"","")
				for i in f.split(","):
					if i not in userlist:
						userlist.append(i)
					else:
						pass
			# print(userlist)
			return userlist
		else:
			print("%s not found!"%(userlist_file))
			return 0

	# def test(self):
	# 	diff=[]
	# 	count=0
	# 	for i in self.getuserlist():
	# 		if i not in diff:
	# 			diff.append(i)
	# 		else:
	# 			print(i)
	# 			count+=1
	# 	print("%s\n%s\n%s"%(diff,count,len(diff))) 

if __name__ == '__main__':
	c=getconf()
	c.get_config()
	print(c.getuserlist(),len(c.getuserlist()))
	# print(c.get_imagepath())