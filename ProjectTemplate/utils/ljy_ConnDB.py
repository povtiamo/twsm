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
execute(op)     执行一个sql语句
fetchone()      取得结果集的下一行
fetchmany(size) 获取结果集的下几行
fetchall()      获取结果集中的所有行
rowcount      返回数据条数或影响行数
close()         关闭游标对象
'''


import psycopg2
import re,time
import ljy_config

class ConnectDB(object):
	def __init__(self):
		self.conf=ljy_config.getconf().get_DB_config()
		self.host=self.conf["dbhost"]
		self.port=self.conf["dbport"]
		self.user=self.conf["dbuser"]
		self.password=self.conf["dbpassword"]
		self.database=self.conf["dbdatabase"]
		self.sqlstr=None
		self.conn =self.connTarget()

	def connTarget(self):
		try:
			conn=psycopg2.connect(
				host='%s'%(self.host),
				port=int(self.port),
				user='%s'%(self.user),
				password='%s'%(self.password),
				database='%s'%(self.database))
		except Exception:
			ex=Exception("DB connect False!>'%s:%s<%s>_%s_%s'"%(self.host,self.port,self.database,self.user,self.password))
			raise ex
		print("('%s' connect success!)"%(self.host))
		return conn
	
	def sqlrun(self,sqlstr=None):
		if sqlstr=="" or sqlstr is None:
			sqlstr=self.sqlstr
		result=self.excute_sql(sqlstr)
		return result
	
	def sqlrun_withthread(self,sqlstr=None,saveFile=None):
		if sqlstr=="" or sqlstr is None:
			sqlstr=self.sqlstr
		result=self.excute_sql(sqlstr)
		with open(saveFile,"a",encoding='utf-8') as f:
			nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			result="["+nowtime+"]: "+sqlstr+"\n"+str(result)+"\n-----------------\n"
			# print(result)
			f.write(str(result))

	def excute_sql(self,sqlstr=None):
		cursor = self.conn.cursor()
		count=0
		try:
			# print(sqlstr)
			cursor.execute(sqlstr)
			count=cursor.rowcount
			# print("execute:",count)
		except Exception as e:
			self.conn.rollback()
			self.conn.close()
			raise Exception("SQLstr run False！:\n'%s'\n%s"%(sqlstr,e))
		try:
			rs = cursor.fetchall()
			# print(rs)
			if len(rs) <1:
				return None
			else:
				return rs
		except:
			# print("rs is None:",count)
			return "%s rows changed"%(count)

	def DBquit(self):
		self.conn.commit()
		print("('%s' close done!)"%(self.host))
		self.conn.close()


if __name__ == '__main__':
	class test(ConnectDB):
		def __init__(self):
			ConnectDB.__init__(self)
			self.host="localhost"
			self.port=5432
			self.user="postgres"
			self.password="postgres"
			self.database="aidata"
			self.sqlstr="select *from app_d_js_jbxxdbtj;"
			self.conn =self.connTarget()

		def testSQL(self):
			print(self.sqlrun(self.sqlstr))

	t=test()
	t.testSQL()
	t.DBquit()