''' 
* @Author: lijiayi  
* @Date: 2019-07-02 15:05:36  
* @Last Modified by:   lijiayi  
* @Last Modified time: 2019-07-02 15:05:36  
'''
#!/usr/bin/python
#-*-coding:utf-8-*-
'''
connection对象支持的方法
cursor()        使用该连接创建并返回游标
commit()        提交当前事务
rollback()      回滚当前事务
close()         关闭连接

cursor对象支持的方法
execute(op)     执行一个数据库的查询命令
fetchone()      取得结果集的下一行
fetchmany(size) 获取结果集的下几行
fetchall()      获取结果集中的所有行
rowcount()      返回数据条数或影响行数
close()         关闭游标对象
'''


import psycopg2
import re

class ConnectDB(object):
	def __init__(self,conn,*args):
		self.conn =conn
		# self.find_str=args[0]

#get messages
	def get_twpaasMSG(self):
		try:
			return self.t_e_msg_history()
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()
			print(str(e))
			raise e

#Tables
	def t_e_msg_history(self):
		cursor = self.conn.cursor()
		try:
			sql = "SELECT notifycontent FROM public.t_e_msg_history WHERE notifyreceiver='%s' ORDER BY reqtime DESC LIMIT'1'" %(self.find_str)
			# print(sql)
			cursor.execute(sql)
			rs = cursor.fetchall()
			# print(rs)
			if len(rs) <1:
				raise Exception("号码'%s'获取验证码失败" %(self.find_str))
			pattern = re.compile(r'\d+')
			result = pattern.findall(str(rs))[0]
		finally:
			cursor.close()
		return result

	def t_jx_user_logininfo(self):
		cursor = self.conn.cursor()
		try:
			sql = "SELECT orgid FROM vocationalenroll.t_jx_user_logininfo WHERE registrationno='%s' ORDER BY lastlogintime DESC LIMIT'1'" %(self.find_str)
			# print(sql)
			cursor.execute(sql)
			rs = cursor.fetchall()
			# print(rs)
			if len(rs) <1:
				raise Exception("账号'%s'获取登录信息失败" %(self.find_str))
			pattern = re.compile(r'\d+')
			result = pattern.findall(str(rs))[0]
			# print(result)
		finally:
			cursor.close()
		return result

	def t_e_student(self):
		cursor = self.conn.cursor()
		level=1
		aiclass=1
		student=1
		for l in range(level):
			for a in range(aiclass):
				for s in range(student):
					
					name="s_bat221613_%s_%s_%s"%(l+1,a+1,s+1)
					try:
						sql = "select * from t_e_student WHERE name = 's_bat221613_%s年级%s班%s学生'" %(l+1,a+1,s+1)
						# sql = "update t_e_student set name='%s' WHERE name = 's_bat221613_%s年级%s班%s学生'" %(name,l+1,a+1,s+1)
						print(sql)
						cursor.execute(sql)
						rs = cursor.fetchall()
						print(rs)
						if len(rs) <1:
							raise Exception("账号'%s'error" %(self.find_str))
						pattern = re.compile(r'\d+')
						result = pattern.findall(str(rs))[0]
						# print(result)
					finally:
						cursor.close()
		return result

def connTarget(host=None,port=None,user=None,password=None,database=None):
	conn=psycopg2.connect(
		host='%s'%(host),
		port=int(port),
		user='%s'%(user),
		password='%s'%(password),
		database='%s'%(database))
	return conn	

def e000001():
	conn=psycopg2.connect(
		host='192.168.102.11',
		port=8832,
		user='e000001',
		password='e000001',
		database='e000001')
	return conn


def aischool():
	conn=psycopg2.connect(
		host='192.168.130.40',
		port=8832,
		user='aischool',
		password='okITj55wzEQfR_LMkC4K_sofXXTq44YH',
		database='aischool')
	return conn

def twpaasDB():
	#连接数据库 MySql
	'''conn = pymysql.Connect(
		host='localhost',
		port=3306,
		user='root',
		passwd='root',
		db='OtkDb',
		charset='utf8')'''
	#连接数据库PostgreSQL
	conn=psycopg2.connect(
		host='192.168.102.11',
		port=8832,
		user='twpaas',
		password='twpaasuseR@2017',
		database='twpaas')
	return conn

def getDBconn(self):
	import ljy_config
	conf=ljy_config.getconf().get_config()
	return connTarget(conf["DBhost"],conf["DBport"],conf["DBuser"],conf["DBpassword"],conf["DBdatabase"])

if __name__ == '__main__':
	conn=aischool()
	a=ConnectDB(conn)
	a.t_e_student()