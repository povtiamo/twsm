#!/usr/python
# coding=utf-8
import os, time, hashlib, json, codecs, sys

# 临时文件存放位置
PATH  = sys.argv[1]

# 统计数量
def countFiles(dirPath):
    print dirPath
    os.system("cd %s; ls -lR|grep '^-'|wc -l" % (dirPath))

# 遍历文件夹
def getFile(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                countFiles(full_path)
    except Exception, ex:
        print ex

def main():
    getFile(PATH)

main()