#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import stat
import logging
import time

class CustomLogger:
    """对SQL文件解析，替换变量，然后传入数据库中执行"""

    def __init__(self,script_path,cycle_id,parallel_id):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        #自定义文件handler
        date_str = time.strftime('%Y%m%d',time.localtime(time.time()))
        time_str = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        cycle_str = cycle_id[0:10].replace('-','')

        (file_path,temp_file_name) = os.path.split(script_path)
        (shot_name,extension) = os.path.splitext(temp_file_name)
        self.job_msg_context = 'job[' + shot_name + ']' + ' cycle[' + cycle_id + ']' + ' parallel_id[' + parallel_id + ']'
        log_path = file_path+'/'+date_str+'/'+shot_name[0:3].lower()+'/'+shot_name.lower()+'/'
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
            os.chmod(log_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
        log_file = log_path+'/'+shot_name+'_'+cycle_str+'_'+parallel_id+'_'+time_str+'.log'

        data_format = '%Y-%m-%d %H:%M:%S'
        msg_format = '%(asctime)s %(job_msg)s %(levelname)s: %(message)s'
        file_formatter = logging.Formatter(fmt=msg_format,datefmt=data_format)

        file_handler = logging.FileHandler(log_file,'w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        #自定义控制台handler
        msg_format = '%(asctime)s %(job_msg)s %(levelname)s: %(message)s'
        console_formatter = logging.Formatter(fmt=msg_format,datefmt=data_format)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)

        #添加handler
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


    def debug(self,msg):
        self.logger.debug(msg,extra={'job_msg':self.job_msg_context})

    def info(self,msg):
        self.logger.info(msg,extra={'job_msg':self.job_msg_context})

    def warning(self,msg):
        self.logger.warning(msg,extra={'job_msg':self.job_msg_context})

    def error(self,msg):
        self.logger.error(msg,extra={'job_msg':self.job_msg_context})

    def critical(self,msg):
        self.logger.critical(msg,extra={'job_msg':self.job_msg_context})


if __name__ == '__main__':

    sql_file_path = '/var/lib/hive/liuym/SQLScripts/TMP_STD_BASIC_INFO_D.HQL'

    my_logger = CustomLogger(sql_file_path,'2018-10-10')
    my_logger.debug('debug message ....')
    my_logger.info('info message ....')
    my_logger.warning('warning message ....')
    my_logger.error('error message ....')
    my_logger.critical('critical message ....')
