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
		self.conf = configparser.ConfigParser()
		self.conf.read(self.get_config_path(),encoding="utf-8-sig")

	def get_config_path(self):
		return os.getcwd()+"\\conf.ini"

	def get_config(self):
		conf_dict={}
		try:
			conf_dict.update(dict(self.conf["info"]))
			conf_dict.update(dict(self.conf["path"]))
			conf_dict.update(dict(self.conf["sys"]))
			conf_dict.update(dict(self.conf["custommethod"]))
		except Exception as e:
			import traceback
			traceback.print_exc()
			print("读取conf.ini出错，注意格式是否正确，以及%是否转义;;;read conf.ini error，plz check out")
			sys.exit()
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

	def getuserlist(self):
		conf=self.get_config()
		userlist=[]
		userlist_file=os.getcwd()+"\\"+conf["userlistfile"]
		with open(userlist_file,"rb") as f:
			#replace替换文档中的换行
			f=f.read().decode('utf-8').replace("\n","").replace("\r","").replace("\t","").replace("\"","")
			for i in f.split(","):
				if i not in userlist:
					userlist.append(i)
				else:
					pass
		# with open(userlist_file,"wb") as f:
		# 	f.write(str(userlist).encode('utf-8'))
		return userlist

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
	# print(c.getuserlist(),len(c.getuserlist()))
	print(c.get_imagepath())