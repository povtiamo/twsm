#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import re
import time
import pdb
import ConfigParser

reload(sys)
sys.setdefaultencoding( "utf-8" )

sys.path.append(os.path.split(os.path.abspath(sys.argv[0]))[0]+"/../Database")
sys.path.append(os.path.split(os.path.abspath(sys.argv[0]))[0]+"/../Log")
from DBFactory import DBFactory
from CustomLogger import CustomLogger
from DBLogger import DBLogger
from PreOperator import PreOperator

class JobParser:
    """对SQL文件解析，替换变量，然后传入数据库中执行"""

    def __init__(self,sql_file,cycle_id,parallel_id,logger):
        self.sql_file    = sql_file
        self.cycle_id    = cycle_id
        self.parallel_id = parallel_id
        self.logger      = logger

        (file_path,temp_file_name) = os.path.split(sql_file)
        (shot_name,extension) = os.path.splitext(temp_file_name)
        self.log_dict = {}
        self.log_dict['job_name']    = shot_name
        self.log_dict['cycle_id']    = cycle_id
        self.log_dict['parallel_id'] = parallel_id
        self.log_dict['script_path'] = sql_file
        self.log_dict['start_time']  = time.strftime("%Y%m%d %H:%M:%S", time.localtime())

        self.del_tab_list = []

    def check_job(self):
        '''执行任务前对是否满足执行条件进行检查'''
        self.logger.info(u'--------->任务运行前进行检查...')
        pre_oper = PreOperator(logger)
        (self.msg_code,self.msg_info) = pre_oper.run(self.log_dict)
        if self.msg_code in (-1,1,-2) :
            self.log_dict['run_status']  = self.msg_code #运行状态：0-成功，-1-失败，-2-同一个任务多个脚本运行，1-依赖未完成
            self.log_dict['log_msg']     = self.msg_info
            self.write_log()


    def run(self,argv_dict):
        '''执行SQL任务主体'''
        self.logger.info(u'--------->解析SQL,执行任务主体')
        #读出SQL文件内容，并把SQL语句拆分
        with open(self.sql_file,'r') as op:
            sql_context = op.read()
        sql_lists = sql_context.split(';')
	set_lists = []
        #取得一个数据库的连接,依次执行SQL语句
        db_oper = DBFactory(self.logger).create('spark_for_aidata')
        for sql_str in sql_lists:

            # 参数替换
            for argv_key in argv_dict.keys():
                sql_str = str.replace(sql_str,'${'+argv_key+'}',argv_dict[argv_key])

            # 取出临时表的删除语句
            sql_str = sql_str.strip().decode(encoding='utf-8')
            match_ojb = re.search(r'^\s*drop\s+table\s+if\s+exists.*',sql_str,re.M|re.I)
            if match_ojb :
                self.del_tab_list.append(match_ojb.group().strip())

            # 执行语句
            (self.msg_code,self.msg_info)=db_oper.excute_sql(sql_str)  #执行SQL语句
            if self.msg_code != 0 :
                break

        db_oper.close_connection()

    def del_tmp_tabs(self,del_tmp_flag='1'):
        '''删除脚本中创建的临时表,默认是删除'''
        if del_tmp_flag == '0' or self.msg_code != 0:
            return

        self.logger.info(u'--------->删除脚本中创建的临时表')
        #取得一个数据库的连接,依次执行SQL语句
        db_oper = DBFactory(self.logger).create('spark_for_aidata')
        for del_tab_str in self.del_tab_list:
            (self.msg_code,self.msg_info)=db_oper.excute_sql(del_tab_str)  #执行SQL语句
            if self.msg_code != 0 :
                break
        db_oper.close_connection()

    def write_log(self):
        '''写日志并退出'''
        self.logger.info(u'--------->任务执行完成，写入数据库日志')
        self.log_dict['run_status']  = self.msg_code #运行状态：0-成功，-1-失败，-2-同一个任务多个脚本运行，1-依赖未完成
        self.log_dict['log_msg']     = self.msg_info
        #DBLogger(logger).run(self.log_dict)  #写数据库日志
        if self.msg_code in (-1,-2):
            self.logger.error(self.msg_info)  #写文件日志
        elif self.msg_code == 1 :
            self.logger.warning(self.msg_info)  #写文件日志
        else :
            self.logger.info(self.msg_info)   #写文件日志
        exit(self.msg_code)
    def merge_tab(self,merge_flag='1'):
        """在程序最后面对目标表进行小文件合并，如建表未按标准创建会直接退出"""
        if merge_flag == '0' or self.msg_code != 0:
            return
        self.logger.info(u'--------->开始合并表中的小文件')
        
        #取得一个数据库的连接        
        db_oper = DBFactory(self.logger).create('spark_for_aidata')
        try:
            job_name = self.log_dict['job_name']
            tmp_table_name = 'TMP_' + job_name
            table_name = job_name[0:3].replace('REP','APP') + '.' + job_name
            	
            #判断分区
            if table_name[-1:].upper() == 'D':
                par_cycle_id = 'p_day_id'
            elif table_name[-1:].upper() == 'M':
                par_cycle_id = 'p_mon_id'
            else :
                return
                
            db_oper.hc.sql('SET hive.exec.dynamic.partition.mode=nostrict')            
            sql = 'select * from ' + table_name
            self.logger.info(sql)
            df = db_oper.hc.sql(sql) #将全表读回内存，创建dataframe
            #对dataframe重新分区并创建临时表
            df.coalesce(1).persist().createOrReplaceTempView(tmp_table_name)
            sql = 'INSERT overwrite TABLE %s partition (%s,p_lan_id)SELECT * FROM %s' % (table_name,par_cycle_id,tmp_table_name)
            self.logger.info(sql)
            df = db_oper.hc.sql(sql) #数据重新插入结果表
        except Exception as e:
            self.logger.warning(u'--------->小文件合并失败')
            self.logger.error(e.message)
        finally:
            db_oper.close_connection()

def show_usage_msg():
    msg_info = u'''
    检查入参是否正确，脚本运行格式如下：
    python ${JOB_HOME}/JobParser/JobParser.py  /xxx/yyy.conf cycle_id=yyyy-mm-dd [lan_id=xxxxxx ...]
    '''
    print(msg_info)
    exit(-1)

def run_job(argv_list=sys.argv):
    # 取得SQL文件路径
    job_conf_file = argv_list[1]
    (file_path,conf_file_name) = os.path.split(job_conf_file)
    (shot_name,extension) = os.path.splitext(conf_file_name)
    job_log_file = os.path.split(os.path.abspath(argv_list[0]))[0]+'/../../Logs/'+shot_name

    argv_dict = {}
    job_sql_file = file_path + '/' + shot_name + '.HQL'

    # 取得配置文件中的参数
    if len(argv_list) >= 3:
        global_parser = ConfigParser.SafeConfigParser()
        global_parser.read('/data/etl_home/ETLScripts/SQLScripts/jobs_global.conf')  # 针对现场进行修改
        for item in global_parser.items('DEFAULT'):
            argv_dict[item[0]]=item[1]

        job_parser = ConfigParser.SafeConfigParser()
        print(job_conf_file)
        job_parser.read(job_conf_file)
        for item in job_parser.items('CUSTOM'):
            argv_dict[item[0]]=item[1]

        for input_str in argv_list[2:]:
            if not input_str.find('='):
                show_usage_msg()

            (item_name,item_val) = input_str.split('=')
            argv_dict[item_name]=item_val

        argv_dict['parallel_id'] = argv_dict['lan_id']

        print(u'脚本参数列表如下：')
        for each_argv in argv_dict:
            print(u'    ' + each_argv.decode('utf-8') + ' = ' + argv_dict[each_argv].decode('utf-8'))
    else:
        show_usage_msg()

    logger = CustomLogger(job_log_file,argv_dict['cycle_id'],argv_dict['parallel_id'])
    job = JobParser(job_sql_file,argv_dict['cycle_id'],argv_dict['parallel_id'],logger)
    #job.check_job()
    job.run(argv_dict)
    job.del_tmp_tabs(argv_dict['del_tmp_flag'])
    job.merge_tab()
    job.write_log()

if __name__ == '__main__':
    run_job()
    exit(0)
