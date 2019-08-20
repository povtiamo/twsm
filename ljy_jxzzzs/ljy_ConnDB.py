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
		self.find_str=args[0]

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


def e000001():
	conn=psycopg2.connect(
		host='192.168.102.11',
		port=8832,
		user='e000001',
		password='e000001',
		database='e000001')
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

if __name__ == '__main__':
	conn=twpaasDB()
	a=ConnectDB(conn,'13662539542')
	print(a.get_twpaasMSG())
