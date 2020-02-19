#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuym'

import os
import sys
import time
import datetime
from dateutil.relativedelta import relativedelta
import ConfigParser
import commands
import JobParser

reload(sys)
sys.setdefaultencoding( "utf-8" )

def create_run_arguments():
    conf_path    = sys.argv[1]
    cycle_id     = sys.argv[2]
    cycle_format = sys.argv[3]
    mon_offset   = sys.argv[4]
    day_offset   = sys.argv[5]
    lan_id       = sys.argv[6]

    months = relativedelta(months=int(mon_offset))
    days   = relativedelta(days=int(day_offset))

    if cycle_id == '0':
        cycle_id = (datetime.datetime.now() + months + days).strftime(str(cycle_format))

    read_parser = ConfigParser.SafeConfigParser()
    write_parser = ConfigParser.SafeConfigParser()

    arguments = []
    arguments.append('cycle_id=' + cycle_id)
    arguments.append('lan_id=' + lan_id)

    return arguments


if __name__ == '__main__':
    other_arguments = create_run_arguments()

    argv_list = []
    argv_list.append(os.path.split(os.path.abspath(sys.argv[0]))[0]+"/JobParser.py")
    argv_list.append(sys.argv[1])
    argv_list.extend(other_arguments)
    JobParser.run_job(argv_list)
    exit(0)
