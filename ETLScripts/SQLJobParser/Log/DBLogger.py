#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import re
sys.path.append("../Database")
from DBFactory import DBFactory
from CustomLogger import CustomLogger

class DBLogger:
    """对SQL文件解析，替换变量，然后传入数据库中执行"""

    def __init__(self,logger):
        self.etl_msg_cpt = 'etl.etl_msg_cpt' #调度成功消息表
        self.etl_msg_his = 'etl.etl_msg_his' #调度历史消息表
        self.etl_msg_err = 'etl.etl_msg_err' #调度异常消息表
        self.logger      = logger
        self.log_flag    = '0'  #是否把日志写库的过程信息以日志形式显示出来

        #取得一个数据库的连接,日志数据库使用关系数据库
        self.db_oper = DBFactory(self.logger).create('pgsql_for_log')

    def run(self,log_dict):
        self.job_name    = log_dict.get('job_name')
        self.cycle_id    = log_dict.get('cycle_id')
        self.parallel_id = log_dict.get('parallel_id')
        self.run_status  = log_dict.get('run_status')
        self.log_msg     = log_dict.get('log_msg')
        self.script_path = log_dict.get('script_path')
        self.start_time  = log_dict.get('start_time')

        self.logger.info(u'开始写数据库日志信息')
        res = self.insert_log_msg()
        if res != 0 :
            exit(res)
            self.db_oper.close_connection()  #关闭数据库
        self.logger.info(u'完成写数据库日志信息')
        self.db_oper.close_connection()  #关闭数据库

    def insert_log_msg(self) :
        '''\
        Function: 把日志信息写入日志表中
        Date    : 2018-03-15 16:01:29
        Author  : Liuym
        Notes   : 把操作的日志信息按规则分别写入历史表，异常表，成功表
        Argvs   : 无
        Result  : 无，遇到运行错误直接退出程序
        '''
        #调度历史消息表,用于观察历史运行情况，不做删除操作，数据清除考虑人工清理
        sql_str = u"""\
        insert into {etl_msg_his}
             ( cycle_id    -- 账期
              ,mon_id      -- 月份
              ,parallel_id -- 并发ID
              ,job_name    -- 任务名
              ,log_msg     -- 消息内容
              ,script_path -- 脚本路径
              ,run_status  -- 运行状态：0-成功，-1-失败，-2-同一个任务多个脚本运行，1-依赖未完成
              ,start_time  -- 开始时间
              ,end_time    -- 结束时间
             )
        select '{cycle_id}'
              ,substr('{cycle_id}',1,7)
              ,'{parallel_id}'
              ,'{job_name}'
              ,'{log_msg}'
              ,'{script_path}'
              ,'{run_status}'
              ,to_date('{start_time}','YYYYMMDD HH24:MI:SS')
              ,now()
          from (select 'x') t
         where {run_status}  <> '1'
        ;
        """
        sql_str = sql_str.format(etl_msg_his  = self.etl_msg_his  ,\
                                 cycle_id     = self.cycle_id     ,\
                                 parallel_id  = self.parallel_id  ,\
                                 job_name     = self.job_name     ,\
                                 log_msg      = self.log_msg      ,\
                                 script_path  = self.script_path  ,\
                                 run_status   = self.run_status   ,\
                                 start_time   = self.start_time)
        self.logger.debug(u'日志插入调度历史消息表，执行SQL语句：\n'+sql_str)
        (msg_code,msg_info) = self.db_oper.excute_sql(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            self.logger.error(u"脚本写日志出错，请核实写日志脚本是否正确。错误信息如下:\n"+msg_info)
            return -1

        #清除成功消息数据
        sql_str = u"""\
        delete from {etl_msg_cpt}
         where mon_id       = substr('{cycle_id}',1,7)
           and cycle_id     = '{cycle_id}'
           and parallel_id  = '{parallel_id}'
           and job_name     = '{job_name}'
           and {run_status} <> '-2'
        ;
        """
        sql_str = sql_str.format(etl_msg_cpt  = self.etl_msg_cpt  ,\
                                 cycle_id     = self.cycle_id     ,\
                                 parallel_id  = self.parallel_id  ,\
                                 job_name     = self.job_name     ,\
                                 run_status   = self.run_status)
        self.logger.debug(u'清除成功消息数据，执行SQL语句：\n'+sql_str)
        (msg_code,msg_info) = self.db_oper.excute_sql(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            self.logger.error(u"脚本写日志出错，请核实写日志脚本是否正确。错误信息如下:\n"+msg_info)
            return -1

        #成功运行脚本_插入成功消息
        sql_str = u"""\
        insert into {etl_msg_cpt}
             ( cycle_id    -- 账期
              ,mon_id      -- 月份
              ,parallel_id -- 并发ID
              ,job_name    -- 任务名
              ,log_msg     -- 消息内容
              ,script_path -- 脚本路径
              ,run_status  -- 运行状态：0-成功，-1-失败，-2-同一个任务多个脚本运行，1-依赖未完成
              ,start_time  -- 开始时间
              ,end_time    -- 结束时间
             )
        select '{cycle_id}'
              ,substr('{cycle_id}',1,7)
              ,'{parallel_id}'
              ,'{job_name}'
              ,'{log_msg}'
              ,'{script_path}'
              ,'{run_status}'
              ,to_date('{start_time}','YYYYMMDD HH24:MI:SS')
              ,now()
          from (select 'x') t
         where {run_status}=0
        ;
        """
        sql_str = sql_str.format(etl_msg_cpt  = self.etl_msg_cpt,\
                                 cycle_id     = self.cycle_id   ,\
                                 parallel_id  = self.parallel_id,\
                                 job_name     = self.job_name   ,\
                                 log_msg      = self.log_msg    ,\
                                 script_path  = self.script_path,\
                                 run_status   = self.run_status ,\
                                 start_time   = self.start_time)
        self.logger.debug(u'插入成功消息，执行SQL语句：\n'+sql_str)
        (msg_code,msg_info) = self.db_oper.excute_sql(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            self.logger.error(u"脚本写日志出错，请核实写日志脚本是否正确。错误信息如下:\n"+msg_info)
            return -1

        #清除调度失败消息表
        sql_str = u"""\
        delete from {etl_msg_err} nologging
         where cycle_id     = '{cycle_id}'
           and parallel_id  = '{parallel_id}'
           and job_name     = '{job_name}'
           and run_status  <> '{run_status}'
        ;
        """
        sql_str = sql_str.format(etl_msg_err  = self.etl_msg_err,\
                                 cycle_id     = self.cycle_id,\
                                 parallel_id  = self.parallel_id   ,\
                                 job_name     = self.job_name,\
                                 run_status   = self.run_status)
        self.logger.debug(u'清除调度失败消息表，执行SQL语句：\n'+sql_str)
        (msg_code,msg_info) = self.db_oper.excute_sql(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            self.logger.error(u"脚本写日志出错，请核实写日志脚本是否正确。错误信息如下:\n"+msg_info)
            return -1

        #更新调度失败消息表
        sql_str = u"""\
        insert into {etl_msg_err}
             ( cycle_id    -- 账期
              ,parallel_id -- 并发ID
              ,job_name    -- 任务名
              ,log_msg     -- 消息内容
              ,err_cnt     -- 错误次数
              ,run_status  -- 运行状态：0-成功，-1-失败，-2-同一个任务多个脚本运行，1-依赖未完成
              ,start_time  -- 开始时间
              ,end_time    -- 结束时间
             )
        select cycle_id
              ,parallel_id
              ,job_name
              ,'{log_msg}'
              ,sum(err_cnt)
              ,'{run_status}'
              ,to_date('{start_time}','YYYYMMDD HH24:MI:SS')
              ,now()
          from (select '{cycle_id}'     as cycle_id
                      ,'{parallel_id}'  as parallel_id
                      ,'{job_name}'     as job_name
                      ,max(err_cnt)     as err_cnt
                  from {etl_msg_err}
                 where cycle_id        = '{cycle_id}'
                   and parallel_id     = '{parallel_id}'
                   and job_name        = '{job_name}'
                   and run_status      = '{run_status}'
                   and '{run_status}' <> '0'
                 group by 1,2,3
                 union all
                select '{cycle_id}'     as cycle_id
                      ,'{parallel_id}'  as parallel_id
                      ,'{job_name}'     as job_name
                      ,1                as err_cnt
                  from (select 'x') t
                 where '{run_status}' <> '0'
             ) t
         group by 1,2,3,4,6,7,8
        ;
        """
        sql_str = sql_str.format(etl_msg_err  = self.etl_msg_err,\
                                 cycle_id     = self.cycle_id   ,\
                                 parallel_id  = self.parallel_id,\
                                 job_name     = self.job_name   ,\
                                 log_msg      = self.log_msg    ,\
                                 run_status   = self.run_status ,\
                                 start_time   = self.start_time)
        self.logger.debug(u'更新调度失败消息表，执行SQL语句：\n'+sql_str)
        (msg_code,msg_info) = self.db_oper.excute_sql(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            self.logger.error(u"脚本写日志出错，请核实写日志脚本是否正确。错误信息如下:\n"+msg_info)
            return -1

        #删除原有的失败信息
        sql_str = u"""\
        delete from {etl_msg_err} nologging
         where cycle_id     = '{cycle_id}'
           and parallel_id  = '{parallel_id}'
           and job_name     = '{job_name}'
           and run_status   = '{run_status}'
           and err_cnt      = (select max(err_cnt)-1
                                 from {etl_msg_err}
                                where cycle_id     = '{cycle_id}'
                                  and parallel_id  = '{parallel_id}'
                                  and job_name     = '{job_name}'
                                  and run_status   = '{run_status}')
        ;
        """
        sql_str = sql_str.format(etl_msg_err  = self.etl_msg_err,\
                                 cycle_id     = self.cycle_id,\
                                 parallel_id  = self.parallel_id   ,\
                                 job_name     = self.job_name,\
                                 run_status   = self.run_status)
        self.logger.debug(u'删除原有的失败信息，执行SQL语句：\n'+sql_str)
        (msg_code,msg_info) = self.db_oper.excute_sql(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            self.logger.error(u"脚本写日志出错，请核实写日志脚本是否正确。错误信息如下:\n"+msg_info)
            return -1

        return 0


if __name__ == '__main__':

    sql_file_path = '/var/lib/hive/liuym/SQLScripts/TMP_TEST_LOG.HQL'

    logger = CustomLogger(sql_file_path,'2018-10-10')

    log_dict = {}
    log_dict['job_name']    = 'test_job'
    log_dict['cycle_id']    = '2018-10-10'
    log_dict['parallel_id'] = '410105'
    log_dict['run_status']  = '1' #运行状态：0-成功，-1-失败，-2-同一个任务多个脚本运行，1-依赖未完成
    log_dict['log_msg']     = 'test message..'
    log_dict['script_path'] = '/var/lib/hive/liuym/test_job'
    log_dict['start_time']  = '20181016 19:00:00'

    job = DBLogger(logger).run(log_dict)
