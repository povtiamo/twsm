#!/usr/python
# coding=utf-8
import os, json, codecs

# 临时文件存放位置
save_path  = sys.argv[1]

# 遍历文件夹
def getFile(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                getFile(full_path)
            else:
                print(full_path)
                dir_name = os.path.dirname(full_path)
                file_name = os.path.basename(full_path).split(".")[0]
                
                if file_name == 'package':
                    print "rename : " + file_name
                    new_name = "%s/20001_package.zip"%(dir_name)
                    os.system("mv %s" % (full_path, new_name))
    except Exception, ex:
        print ex  