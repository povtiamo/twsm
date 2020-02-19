#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import json
import re
import ConfigParser

class DBOperator:
    """数据的常用操作类"""

    def __init__(self,database_cat,database_str,logger):
        script_path = os.path.abspath(__file__)
        (file_path,temp_file_name) = os.path.split(script_path)
        conf_database_file = file_path+'/../Conf/DBConnections.conf'

        # 取得配置文件中的数据库连接参数
        cparser = ConfigParser.RawConfigParser()
        cparser.read(conf_database_file)
        self.engine_info = cparser.get(database_cat,database_str)

        #logger.info(u'数据库连接参数初始化完成。')

    def excute_sql(self,sql_str,log_flag='1'):
        '''\
        Function: 执行SQL语句
        Date    : 2018-03-12 16:01:29
        Author  : Liuym
        Notes   : 传入SQL语句字符串，发送到数据库中执行，返回是否成功标识及日志信息
        Argvs   : sql_str -- QL语句字符串
        Result  : msg_code -- 0-成功，-1-失败
                  msg_info -- 日志信息
        '''
        self.msg_code = -1
        self.msg_info = u'日志信息初始值。。'

        self.sql_str = sql_str.strip()
        if self.sql_str != '' and log_flag == '1':
            self.logger.info(u'执行SQL语句\n'+sql_str+'\n')
        self.sql_str = re.sub(r'^\s*--.*','',self.sql_str) #删除注释
        self.sql_str = re.sub(r'\n\s*--.*','\n',self.sql_str).strip() #删除注释
        if self.sql_str == '':
            self.msg_code = 9
            self.msg_info = u"脚本运行成功"

    def get_results(self,sql_str,log_flag='1'):
        '''\
        Function: 获取关系数据库中的结果集
        Date    : 2018-03-13 16:01:29
        Author  : Liuym
        Notes   : 传入SQL语句字符串，发送到数据库中执行，返回是否成功标识，日志信息及结果集
        Argvs   : sql_str -- QL语句字符串
        Result  : msg_code -- 0-成功，-1-失败
                  msg_info -- 日志信息
                  results  -- 结果集
        '''
        self.msg_code = -1
        self.msg_info = u'日志信息初始值。。'
        self.record_list = u'结果集初始值。。'

        self.sql_str = sql_str.strip()
        if self.sql_str != '' and log_flag == '1':
            self.logger.info(u'执行查询SQL语句\n'+sql_str+'\n')
        self.sql_str = re.sub(r'^\s*--.*','',self.sql_str) #删除注释
        self.sql_str = re.sub(r'\n\s*--.*','\n',self.sql_str).strip() #删除注释
        if self.sql_str == '':
            self.msg_code = 9
            self.msg_info = u"脚本运行成功"

    def close_connection(self):
        '''\
        Function: 关闭数据库的连接
        Date    : 2018-10-11 16:01:29
        Author  : Liuym
        Notes   : 关闭数据库的连接，释放资源
        '''
        pass

if __name__ == '__main__':
    db_oper = DBOperator('PGSQL')
    print(db_oper.excute_sql('xxxx'))
    print(db_oper.get_results('xxxxxxx'))
    print(db_oper.engine_info)
