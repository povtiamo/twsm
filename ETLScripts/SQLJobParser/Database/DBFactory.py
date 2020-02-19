#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
from DBOperator import DBOperator
from PostgresqlOperator import PostgresqlOperator
from SparkOperator import SparkOperator
from MysqlOperator import MysqlOperator

class DBFactory:
    """根据入参返回不同的数据操作实例"""

    def __init__(self,logger):
        self.logger = logger

    def create(self, database_str):
        if database_str.upper().startswith('SPARK') :
            return SparkOperator('SPARK',database_str,self.logger)
        elif database_str.upper().startswith('PGSQL') :
            return PostgresqlOperator('PGSQL',database_str,self.logger)
        elif database_str.upper().startswith('MYSQL') :
            return MysqlOperator('MYSQL',database_str,self.logger)
        else :
            self.logger.error(u'未支持的数据库操作,目前仅支持数据类型：SPARK,PGSQL,MYSQL')
            exit(-1)




if __name__ == '__main__':
    db_oper = DBFactory().create('SPARK')

    (msg_code,msg_info)=db_oper.excute_sql("insert into wid_lym1.lym_tmp values('1111','这是一条测试数据')")
    print("==================================================")
    print("msg_code:"+str(msg_code))
    print("msg_info:"+msg_info)

    (msg_code,msg_info,record_list)=db_oper.get_results("select concat(str1,'串'),str2 from wid_lym1.lym_tmp")
    record_list2 = record_list
    for list_str in record_list2 :
      for str in list_str:
        print(str),
      print('')

    db_oper.close_connection()
