'''
 * @Author: lijiayi 
 * @Date: 2019-06-28 11:57:17 
 * @Last Modified by: lijiayi
 * @Last Modified time: 2019-06-28 13:45:54
 '''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

import os,time
import sys
import traceback
import threading

# 获取项目的目录
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把path加入环境变量，0表示放在最前面，因为python解释器会按照列表顺序去依次到每个目录下去匹配你要导入的模块名，
# 只要在一个目录下匹配到了该模块名，就立刻导入，不再继续往后找
sys.path.insert(0, path)

try:
	from utils import ljy_run,ljy_config
except Exception:
	ex=Exception("Package utils import False!")
	raise ex

# try:
# 	os.chdir(os.path.dirname(sys.argv[0]))
# except:
# 	pass

c=ljy_config.getconf().get_config()

try:
	for i in range(int(c["loop"])):
		passwd=c["passwd"]
		username=""
		start_time=time.time()
		a=ljy_run.common(i,username,passwd,start_time)
		target=threading.Thread(target=a.main)
		#threading.active_count()线程数量,手动限制每次开启的线程数量
		while threading.active_count()>int(c["thread"]):
			time.sleep(10)
		target.start()
		#threading.Thread.__stop()

except KeyboardInterrupt:
	print("key break!")
	sys.exit()

