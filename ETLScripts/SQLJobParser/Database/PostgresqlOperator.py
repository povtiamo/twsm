#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --========================================================================================--
# @ClassDesc: DB2的常用操作类
# @Date    : 2018-03-12 14:13:35
# @Author  : Liuym
# @Comment : 2018-03-12 14:13:35 create file

# --========================================================================================--

import os
import sys
sys.path.append("../Log")
from CustomLogger import CustomLogger
from DBOperator import DBOperator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib import quote_plus as urlquote
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext, Row

class PostgresqlOperator(DBOperator):
    """Postgresql操作类"""

    def __init__(self,database_cat,database_str,logger):
        '''\
        初始化一个连接
        '''
        DBOperator.__init__(self,database_cat,database_str,logger)

        engine = create_engine(self.engine_info)  #初始化数据库连接 echo=True
        DBsesion = sessionmaker(bind=engine) #创建DBSession类型
        self.session = DBsesion() #建session对象
        self.logger = logger
        self.logger.info(u'Postgresql 连接成功。')

    def excute_sql(self,sqlstr,log_flag='1'):
        '''\
        Function: 关系型数据中执行SQL语句函数
        Date    : 2018-03-12 16:01:29
        Author  : Liuym
        Notes   : 传入SQL语句字符串，发送到数据库中执行，返回是否成功标识及日志信息
        Argvs   : sqlstr -- QL语句字符串
        Result  : msg_code -- 0-成功，-1-失败
                  msg_info -- 日志信息
        '''
        DBOperator.excute_sql(self,sqlstr,log_flag)

        #若SQL语句为空，跳过实际执行。
        if self.msg_code == 9 :
            return (0,self.msg_info)

        try:
            self.session.execute(self.sql_str)
        except Exception as e:
            self.session.rollback()
            self.msg_code = -1
            self.msg_info = u"SQL语句执行错误："+str(e).replace("\'","\"")[0:3000]
        else:
            self.session.commit()
            self.msg_code = 0
            self.msg_info = u"脚本运行成功"

        return (self.msg_code,self.msg_info)

    def get_results(self,sqlstr,log_flag='1'):
        '''\
        Function: 获取关系数据库中的结果集
        Date    : 2018-03-13 16:01:29
        Author  : Liuym
        Notes   : 传入SQL语句字符串，发送到数据库中执行，返回是否成功标识，日志信息及结果集
        Argvs   : sqlstr -- QL语句字符串
        Result  : msg_code -- 0-成功，-1-失败
                  msg_info -- 日志信息
                  results  -- 结果集
        '''
        DBOperator.get_results(self,sqlstr,log_flag)

        #若SQL语句为空，跳过实际执行。
        if self.msg_code == 9 :
            return (0,self.msg_info)

        try:
            self.results = self.session.execute(self.sql_str)
            self.record_list=self.results.fetchall()
        except Exception as e:
            self.session.rollback()
            self.msg_code = -1
            self.msg_info = u"SQL语句执行错误："+str(e).replace("\'","\"")[0:3000]
        else:
            self.session.commit()
            self.msg_code = 0
            self.msg_info = u"脚本运行成功"

        return (self.msg_code,self.msg_info,self.record_list)

    def close_connection(self):
        '''\
        Function: 关闭数据库的连接
        Date    : 2018-10-11 16:01:29
        Author  : Liuym
        Notes   : 关闭数据库的连接，释放资源
        '''
        DBOperator.close_connection(self)
        self.session.close()
        self.logger.info(u'Postgresql 断开连接。')

if __name__ == '__main__' :

    sql_str0="""\
    DROP TABLE IF EXISTS tmp.lym_tmp
    """

    sql_str1="""\
    create table tmp.lym_tmp (
     str1 int
    ,str2 varchar(200)
    )
    """

    sql_str2="""\
    insert into tmp.lym_tmp values(333,'这是一条测试数据2222')
    """

    sql_str3="""\
    select concat(str1,'串'),str2 from tmp.lym_tmp
    """

    sql_file_path = '/var/lib/hive/liuym/SQLScripts/TMP_STD_BASIC_INFO_D.HQL'
    logger = CustomLogger(sql_file_path,'2018-10-10')

    pgsql_oper=PostgresqlOperator('PGSQL',logger)
    #(msg_code,msg_info)=pgsql_oper.excute_sql(sql_str0)
    #logger.info("==================================================")
    #logger.info("msg_code:"+str(msg_code))
    #logger.info("msg_info:"+msg_info)

    #(msg_code,msg_info)=pgsql_oper.excute_sql(sql_str1)
    #logger.info("==================================================")
    #logger.info("msg_code:"+str(msg_code))
    #logger.info("msg_info:"+msg_info)

    #(msg_code,msg_info)=pgsql_oper.excute_sql(sql_str2)
    #logger.info("==================================================")
    #logger.info("msg_code:"+str(msg_code))
    #logger.info("msg_info:"+msg_info)

    (msg_code,msg_info,record_list)=pgsql_oper.get_results(sql_str3)
    record_list2 = record_list
    for list_str in record_list2 :
      for str in list_str:
        logger.info(str),
      logger.info('')

    pgsql_oper.close_connection()
