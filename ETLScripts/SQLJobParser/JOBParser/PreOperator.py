#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import re
sys.path.append("../Database")
from DBFactory import DBFactory
from CustomLogger import CustomLogger

class PreOperator:
    """执行任务前进行预处理操作"""

    def __init__(self,logger):
        self.etl_msg_cpt      = 'etl.etl_msg_cpt'      #调度成功消息表
        self.etl_cycle_type   = 'etl.etl_cycle_type'   #依赖判定计算配置表
        self.etl_jobs_rels    = 'etl.etl_jobs_rels'    #调度依赖关系表
        self.etl_parallel_def = 'etl.etl_parallel_def' #并发定义表
        self.logger      = logger
        self.log_flag    = '0'  #是否以日志形式显示出来


    def run(self,check_dict):
        self.job_name    = check_dict.get('job_name')
        self.cycle_id    = check_dict.get('cycle_id')
        self.parallel_id = check_dict.get('parallel_id')
        self.script_path = check_dict.get('script_path')

        #取得一个数据库的连接
        self.db_oper = DBFactory(self.logger).create('pgsql_for_etl')
        self.logger.info(u'检查判断是否由多个脚本写入同一个目标表')
        (msg_code,msg_info) = self.check_script_path()
        if msg_code != 0 :
            self.db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        self.logger.info(u'检查依赖任务是否已经完成')
        (msg_code,msg_info) = self.check_condition()
        if msg_code != 0 :
            self.db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        self.db_oper.close_connection()  #关闭数据库
        self.logger.info(msg_info)

        if self.job_name.upper().endswith('_L'):
            self.logger.info(u'对历史拉链表进行数据回滚')
            (msg_code,msg_info) = self.data_rollback()
            if msg_code != 0 :
                return (msg_code,msg_info)
            self.logger.info(msg_info)

        return (msg_code,msg_info)

    def check_script_path(self):
        '''\
        Function: 检查判断是否由多个脚本写入同一个目标表
        Date    : 2018-10-16 16:01:29
        Author  : Liuym
        Notes   : 检查判断是否由多个脚本写入同一个目标表，通过判定结果改写日志信息
        Argvs   : 无
        Result  : msg_code -- 0-成功，-1-失败，-2-一个任务多个路径
                  msg_info -- 日志信息
        '''
        sql_str = u"""\
        select count(1)
          from {etl_msg_cpt}
         where mon_id       =  substr('{cycle_id}',1,7)
           and cycle_id     =  '{cycle_id}'
           and parallel_id  =  '{parallel_id}'
           and job_name     =  '{job_name}'
           and script_path  <> '{script_path}'
        ;
        """
        sql_str = sql_str.format(etl_msg_cpt  = self.etl_msg_cpt,\
                                 cycle_id     = self.cycle_id   ,\
                                 parallel_id  = self.parallel_id,\
                                 job_name     = self.job_name   ,\
                                 script_path  = self.script_path)
        (msg_code,msg_info,record_list) = self.db_oper.get_results(sql_str,log_flag=self.log_flag)
        cnt = record_list[0][0]
        if cnt != 0 :
            msg_code = -2
            msg_info = u"该任务已由另一个脚本调度运行，具体请查看日志信息表："+self.etl_msg_cpt

        return (msg_code,msg_info)

    def check_condition(self) :
        '''\
        Function: 检查任务运行前置条件
        Date    : 2018-03-15 16:01:29
        Author  : Liuym
        Notes   : 检查任务是否已经满足往下运行
        Argvs   : 无
        Result  : msg_code -- 0-成功，-1-失败，1-条件不满足
                  msg_info -- 日志信息
        '''
        #取出当前表依赖表列表
        sql_str = u"""\
        select trim(job_name         ) as job_name
              ,trim(prev_job_name    ) as prev_job_name
              ,trim(cycle_type       ) as cycle_type
              ,trim(prev_cycle_type  ) as prev_cycle_type
              ,trim(is_parallel_flag ) as is_parallel_flag
              ,offset_flag             as offset
          from {etl_jobs_rels}
         where trim(status) = '00A'
           and upper(trim(job_name)) = upper('{job_name}')
        ;
        """
        sql_str = sql_str.format(etl_jobs_rels  = self.etl_jobs_rels ,\
                                 job_name       = self.job_name)
        (msg_code,msg_info,job_record_list) = self.db_oper.get_results(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            return (msg_code,msg_info)

        if (len(job_record_list) == 0) :
            msg_info = u"当前脚本没有配置依赖信息，请核实！！！！ 依赖配置表： "+self.etl_jobs_rels
            self.logger.warning(msg_info)


        #依次判断依赖的任务是否已经完成
        for i in range(0,len(job_record_list)) :
            job_name         = job_record_list[i][0]
            prev_job_name    = job_record_list[i][1]
            cycle_type       = job_record_list[i][2]
            prev_cycle_type  = job_record_list[i][3]
            is_parallel_flag = job_record_list[i][4]
            offset           = job_record_list[i][5]

            if (len(self.cycle_id) == 16 and cycle_type == "H") or \
               (len(self.cycle_id) == 10 and cycle_type == "D") or \
               (len(self.cycle_id) == 7  and cycle_type == "M") :
                msg_info = u"账期类型与传入的参数校验成功！"
            else :
                msg_code = -1
                msg_info = u"依赖配置表中的账期类型与传入的参数不符，请核实！！"
                return (msg_code,msg_info)

            #取出依赖任务依赖账期的计算表达式
            sql_str = u"""\
            select max(replace(replace(lower(cycle_sql),'&cycle_id&','{cycle_id}'),'&offset&','{offset}'))
                  ,count(1)
                  ,max(upper(cycle_type)||upper(prev_cycle_type))
              from {etl_cycle_type}
             where upper(cycle_type) = upper('{cycle_type}')
               and upper(prev_cycle_type) = upper('{prev_cycle_type}')
            ;
            """
            sql_str = sql_str.format(etl_cycle_type  = self.etl_cycle_type,\
                                     cycle_id        = self.cycle_id      ,\
                                     offset          = offset             ,\
                                     cycle_type      = cycle_type         ,\
                                     prev_cycle_type = prev_cycle_type)
            (msg_code,msg_info,record_list) = self.db_oper.get_results(sql_str,log_flag=self.log_flag)
            if msg_code != 0 :
                return (msg_code,msg_info)

            if record_list[0][1] == 0 :
                msg_code = -1
                msg_info = u"账期依赖类型："+cycle_type+prev_cycle_type+u" 不存在，请在配置表中添加。配置表为："+self.etl_cycle_type
                return (msg_code,msg_info)
            elif record_list[0][1] != 1 :
                msg_code = -1
                msg_info = u"账期依赖类型："+cycle_type+prev_cycle_type+u" 重复配置，请在配置表中核实。配置表为："+self.etl_cycle_type
                return (msg_code,msg_info)

            #计算出依赖任务的依赖账期
            cycle_sql_str = record_list[0][0]
            sql_str = u"""\
            select {cycle_sql_str}
            ;
            """
            sql_str = sql_str.format(cycle_sql_str = cycle_sql_str)
            (msg_code,msg_info,record_list) = self.db_oper.get_results(sql_str,log_flag=self.log_flag)
            if msg_code != 0 :
                return (msg_code,msg_info)

            prev_cycle_id = record_list[0][0]

            #判断依赖是否完成
            sql_str = u"""\
            select count(distinct case when a3.is_parallel_flag='1' -- 当前任务并发,需要判定依赖任务的子任务
                                       then case when a1.is_parallel_flag='1' and a1.parallel_id = '{parallel_id}'
                                                 then a1.parallel_id
                                                 else a1.parallel_id
                                            end
                                       when a3.is_parallel_flag='0' -- 当前任务非并发,需要判定整个依赖任务
                                       then a1.parallel_id
                                  end)    as total_cnt  -- 理念上运行数
                  ,count(case when a2.job_name is not null then a1.parallel_id end)          as run_cnt1 -- 实际运行数
                  ,count(distinct case when a2.job_name is not null then a1.parallel_id end) as run_cnt2 -- 实际运行数(剔重)
                  ,string_agg(case when a2.job_name is null then a1.parallel_id end,',')
              from {etl_parallel_def} a1
              left join {etl_msg_cpt} a2
                on a1.parallel_id = a2.parallel_id
               and a2.cycle_id = '{prev_cycle_id}'
               and upper(a2.job_name)=upper('{prev_job_name}')
              left join (select is_parallel_flag
                           from {etl_parallel_def}
                          where parallel_id = '{parallel_id}'
                 ) a3
                on 1=1
             where a1.is_parallel_flag = '{is_parallel_flag}'
            ;
            """
            sql_str = sql_str.format(etl_msg_cpt      = self.etl_msg_cpt      ,\
                                     etl_parallel_def = self.etl_parallel_def ,\
                                     parallel_id      = self.parallel_id      ,\
                                     prev_cycle_id    = prev_cycle_id         ,\
                                     prev_job_name    = prev_job_name         ,\
                                     is_parallel_flag = is_parallel_flag)
            (msg_code,msg_info,record_list) = self.db_oper.get_results(sql_str,log_flag=self.log_flag)
            if msg_code != 0 :
                return (msg_code,msg_info)

            if record_list[0][0] == 0 :
                msg_code = -1
                msg_info = u"运行的任务的并发ID未定义。请核实定义表："+self.etl_parallel_def
                return (msg_code,msg_info)

            if record_list[0][1] > record_list[0][2] :
                msg_code = -1
                msg_info = u"运行结果重复，请在日志表中核实。"
                return (msg_code,msg_info)

            if record_list[0][0] > record_list[0][2] :
                msg_code = 1
                msg_info = u"依赖任务："+str(prev_job_name)+u" 账期："+str(prev_cycle_id)+u" 并发ID:["+record_list[0][3]+u"] 未运行完成，请核实是否正常运行！！！"
                return (msg_code,msg_info)

        msg_info = u'依赖任务全部完成，脚本继续运行'
        return (msg_code,msg_info)

    def data_rollback(self) :
        '''\
        Function: 历史拉链表数据回滚
        Date    : 2018-10-29 16:01:29
        Author  : Liuym
        Notes   : 统一处理历史拉链表回滚操作，要求历史拉链表表结构统一
        Argvs   : 无
        Result  : msg_code -- 0-成功，-1-失败，1-条件不满足
                  msg_info -- 日志信息
        '''
        metadata_db_oper = DBFactory(self.logger).create('mysql_for_metadata')
        #取出数据库字段列表
        sql_str = u"""\
        SELECT a4.name
              ,a3.tbl_name
              ,a1.column_name
              ,a1.integer_idx
          FROM hive.COLUMNS_V2 a1  -- 字段信息
         INNER JOIN (
               SELECT sd_id
                     ,cd_id
                 FROM hive.SDS
                GROUP BY sd_id,cd_id
             ) a2  -- 文件存储的基本信息
            ON a1.cd_id = a2.cd_id
         INNER JOIN hive.TBLS a3  -- 存储Hive表、视图、索引表的基本信息
            ON a2.sd_id = a3.sd_id
         INNER JOIN hive.DBS a4   -- 数据库的基本信息
            ON a3.db_id = a4.db_id
         WHERE upper(a4.name) = upper(substr('{table_name}',1,3))
           AND upper(a3.tbl_name) = upper('{table_name}')
         ORDER BY 1,2,(integer_idx+0)
        """
        sql_str = sql_str.format(table_name = self.job_name)
        (msg_code,msg_info,record_list) = metadata_db_oper.get_results(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            metadata_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        column_str = ''
        for record in record_list[3:]:
            column_str = column_str + ',' + record[2]
        column_str = column_str[1:]

        #取出需要清除的分区
        sql_str = u"""\
        select a1.name
              ,a2.tbl_name
              ,a3.part_name
              ,a4.end_mon
              ,a4.lan_id
          from hive.DBS a1
         inner join hive.TBLS a2
            on a1.db_id = a2.db_id
         inner join PARTITIONS a3
            on a2.tbl_id = a3.tbl_id
         inner join (
               select part_id
                     ,max(case when integer_idx = '0' then part_key_val end) as end_mon
                     ,max(case when integer_idx = '0' then part_key_val end) as lan_id
                 from hive.PARTITION_KEY_VALS
                group by part_id
             ) a4
            on a3.part_id = a4.part_id
         where upper(a1.name) = upper(substr('{table_name}',1,3))
           and upper(a2.tbl_name) = upper('{table_name}')
           and end_mon >= '{end_mon}'
        """
        sql_str = sql_str.format(table_name = self.job_name   ,\
                                 end_mon    = self.cycle_id[0:7])
        (msg_code,msg_info,record_list) = metadata_db_oper.get_results(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            metadata_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        end_mon_list = []
        for record in record_list:
            end_mon_list.append(record[3])
        metadata_db_oper.close_connection()  #关闭数据库


        data_db_oper = DBFactory(self.logger).create('spark_for_aidata')
        #取出数据表中的最大账期
        sql_str = u"""\
        SELECT nvl(max(start_day),'1900-01-01')
          FROM {table_owner}.{table_name}
         WHERE end_mon = '9999-12'
           AND lan_id  = '{parallel_id}'
        """
        sql_str = sql_str.format(table_owner  = self.job_name[0:3],\
                                 table_name   = self.job_name   ,\
                                 parallel_id  = self.parallel_id)
        (msg_code,msg_info,record_list) = data_db_oper.get_results(sql_str,log_flag=self.log_flag)
        if msg_code != 0 :
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)
        max_cycle_id = record_list[0][0] + ''

        if (max_cycle_id == '' or max_cycle_id < self.cycle_id):
            msg_info = u'数据表中无大于当前账期的数据，不需要进行回滚操作'
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        self.logger.info(u'当前时间点之后被拉成历史的数据回滚成更新前状态')
        sql_str = u"""\
        DROP TABLE IF EXISTS tmp.{table_name}_rollback_{parallel_id}_tmp1
        """
        sql_str = sql_str.format(table_name   = self.job_name   ,\
                                 parallel_id  = self.parallel_id)
        (msg_code,msg_info) = data_db_oper.excute_sql(sql_str,log_flag='1')
        if msg_code != 0 :
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        sql_str = u"""\
        CREATE TABLE tmp.{table_name}_rollback_{parallel_id}_tmp1
            AS
        SELECT start_day       AS start_day      -- 开始日期
              ,CASE WHEN end_day>='{cycle_id}' THEN '9999-12-31'
                    ELSE end_day
               END             AS end_day        -- 结束日期
              ,from_unixtime(unix_timestamp(),'yyyy-MM-dd HH:mm:ss') AS etl_time       -- 数据加载时间
              ,{column_str}
              ,CASE WHEN end_day>='{cycle_id}' THEN '9999-12'
                    ELSE end_mon
               END             AS end_mon        -- 结束月份
              ,lan_id          AS lan_id         -- 行政区
          FROM {table_owner}.{table_name}
         WHERE end_mon >= '{end_mon}'
           AND lan_id  = '{parallel_id}'
        """
        sql_str = sql_str.format(table_owner  = self.job_name[0:3],\
                                 table_name   = self.job_name     ,\
                                 cycle_id     = self.cycle_id     ,\
                                 parallel_id  = self.parallel_id  ,\
                                 end_mon      = self.cycle_id[0:7],\
                                 column_str   = column_str)
        (msg_code,msg_info) = data_db_oper.excute_sql(sql_str,log_flag='1')
        if msg_code != 0 :
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        self.logger.info(u'目标表删除现有表里有效的数据')
        for end_mon_str in end_mon_list :
            sql_str = u"""\
            ALTER TABLE {table_owner}.{table_name} DROP IF EXISTS partition (end_mon='{end_mon_str}',lan_id='{parallel_id}')
            """
            sql_str = sql_str.format(table_owner  = self.job_name[0:3],\
                                     table_name   = self.job_name   ,\
                                     parallel_id  = self.parallel_id,\
                                     end_mon_str  = end_mon_str)
            (msg_code,msg_info) = data_db_oper.excute_sql(sql_str,log_flag='1')
            if msg_code != 0 :
                data_db_oper.close_connection()  #关闭数据库
                return (msg_code,msg_info)

        self.logger.info(u'把更新前有效数据重新放入目标表')
        sql_str = u"""\
        SET hive.exec.dynamic.partition.mode=nostrict
        """
        (msg_code,msg_info) = data_db_oper.excute_sql(sql_str,log_flag='1')
        if msg_code != 0 :
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        sql_str = u"""\
        INSERT OVERWRITE TABLE {table_owner}.{table_name} partition (end_mon,lan_id)
        SELECT *
          FROM tmp.{table_name}_rollback_{parallel_id}_tmp1
         WHERE lan_id = '{parallel_id}'
           AND start_day < '{cycle_id}'
        """
        sql_str = sql_str.format(table_owner  = self.job_name[0:3],\
                                 table_name   = self.job_name     ,\
                                 parallel_id  = self.parallel_id  ,\
                                 cycle_id     = self.cycle_id)
        (msg_code,msg_info) = data_db_oper.excute_sql(sql_str,log_flag='1')
        if msg_code != 0 :
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        sql_str = u"""\
        DROP TABLE IF EXISTS tmp.{table_name}_rollback_{parallel_id}_tmp1
        """
        sql_str = sql_str.format(table_name   = self.job_name   ,\
                                 parallel_id  = self.parallel_id)
        (msg_code,msg_info) = data_db_oper.excute_sql(sql_str,log_flag='1')
        if msg_code != 0 :
            data_db_oper.close_connection()  #关闭数据库
            return (msg_code,msg_info)

        data_db_oper.close_connection()  #关闭数据库
        return (msg_code,msg_info)


if __name__ == '__main__':

    sql_file_path = '/var/lib/hive/liuym/SQLScripts/a.HQL'
    logger = CustomLogger(sql_file_path,'2018-10-10','410105')

    check_dict = {}
    check_dict['job_name']    = sys.argv[1]
    check_dict['cycle_id']    = sys.argv[2]
    check_dict['parallel_id'] = '410105'
    check_dict['script_path'] = '/var/lib/hive/liuym/A.HQL'

    (msg_code,msg_info) = PreOperator(logger).run(check_dict)
    print('msg_code=%s,msg_info=%s' %(msg_code,msg_info))
