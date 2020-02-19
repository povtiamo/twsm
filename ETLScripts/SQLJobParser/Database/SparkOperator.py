#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import pdb
sys.path.append("../Log")
from CustomLogger import CustomLogger
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext, Row
from DBOperator import DBOperator

class SparkOperator(DBOperator):
    """SPARK操作类"""

    def __init__(self,database_cat,database_str,logger):
        '''\
        初始化一个连接
        '''
        DBOperator.__init__(self,database_cat,database_str,logger)

        script_name = __name__
        conf = SparkConf().setAppName(script_name).setMaster("yarn")

        conf.set('spark.executor.instances', '5')
        conf.set('spark.executor.cores', '1')
        conf.set('spark.executor.memory', '2g')
        conf.set('spark.driver.memory', '1g')
        conf.set('spark.sql.shuffle.partitions', '5')
	conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
        conf.set("hive.exec.max.dynamic.partitions","100000")
        conf.set("hive.exec.max.dynamic.partitions.pernode","100000")
        self.sc = SparkContext(conf = conf)
        self.hc = HiveContext(self.sc)
        self.logger = logger
        self.logger.info(u'SPARK 连接成功。')


    def excute_sql(self,sql_str,log_flag='1'):
        '''\
        Function: 在SPARK中执行SQL语句函数
        Date    : 2018-03-12 16:01:29
        Author  : Liuym
        Notes   : 传入SQL语句字符串，发送到SPARK SQL中执行，返回是否成功标识及日志信息
        Argvs   : sql_str -- QL语句字符串
        Result  : msg_code -- 0-成功，-1-失败
                  msg_info -- 日志信息
        '''
        DBOperator.excute_sql(self,sql_str,log_flag)

        #若SQL语句为空，跳过实际执行。
        if self.msg_code == 9 :
            return (0,self.msg_info)

        try:
            self.hc.sql(self.sql_str)
        except Exception as e:
            self.msg_code = -1
            self.msg_info = u"SQL语句执行错误："+str(e).replace("\'","\"")[0:3000]
        else:
            self.msg_code = 0
            self.msg_info = u"脚本运行成功"

        return (self.msg_code,self.msg_info)

    def get_results(self,sql_str,log_flag='1'):
        '''\
        Function: 获取SPARK SQL 中结果集
        Date    : 2018-10-11 16:01:29
        Author  : Liuym
        Notes   : 传入SQL语句字符串，发送到SPARK SQL中执行，返回是否成功标识，日志信息及结果集
        Argvs   : sql_str -- QL语句字符串
        Result  : msg_code -- 0-成功，-1-失败
                  msg_info -- 日志信息
                  results  -- 结果集
        '''
        DBOperator.get_results(self,sql_str,log_flag)

        #若SQL语句为空，跳过实际执行。
        if self.msg_code == 9 :
            return (0,self.msg_info)

        try:
            self.results = self.hc.sql(self.sql_str)  #从SPARK中取得一个DataFrame
            #self.results.cache() # 持久化当前DataFrame
            self.record_list=self.results.rdd.map(lambda line:line.asDict().values()).collect()
        except Exception as e:
            self.msg_code = -1
            self.msg_info = u"SQL语句执行错误："+str(e).replace("\'","\"")[0:3000]
        else:
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
        self.sc.stop()
        self.logger.info(u'SPARK 断开连接。')


if __name__ == '__main__':
    sql_str0="""\
    DROP TABLE IF EXISTS wid_lym1.lym_tmp
    """

    sql_str1="""\
    create table wid_lym1.lym_tmp (
     str1 string
    ,str2 string
    )
    """

    sql_str2="""\
    insert into wid_lym1.lym_tmp values('2222','这是一条测试数据2222')
    """

    sql_str3="""\
    select concat(str1,'串'),str2 from wid_lym1.lym_tmp
    """

    sql_file_path = '/var/lib/hive/liuym/SQLScripts/TMP_STD_BASIC_INFO_D.HQL'
    loggeraaa = CustomLogger(sql_file_path,'2018-10-10')

    spark_oper=SparkOperator('SPARK',loggeraaa)
    #(msg_code,msg_info)=spark_oper.excute_sql(sql_str1)
    #print("==================================================")
    #print("msg_code:"+str(msg_code))
    #print("msg_info:"+msg_info)

    #(msg_code,msg_info)=spark_oper.excute_sql(sql_str2)
    #print("==================================================")
    #print("msg_code:"+str(msg_code))
    #print("msg_info:"+msg_info)

    (msg_code,msg_info,record_list)=spark_oper.get_results(sql_str3)
    record_list2 = record_list
    for list_str in record_list2 :
      for str in list_str:
        print(str),
      print('')

    spark_oper.close_connection()
