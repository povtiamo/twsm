#!/usr/python
# coding=utf-8
import os
from biplist import *

# 需要检查的格式
FileExt = ['ccb']
# 不需要抽查的文件夹
DirExt = []

def packItem(name, width, height, scale):
    item = {
        'scale': scale,
        'name': name,
        'centeredOrigin': False,
        'height': height,
        'width': width,
        'ext': ''
    }
    return item

def reset(xml_path):
    print '修改', xml_path
    plist = readPlist(xml_path)
    items = [
        packItem('iPhone4', 960, 640, 1.0),
        packItem('Android_1920x1080', 1138, 640, 1.0),
        packItem('Android_2160x1080', 1280, 640, 1.0),
        packItem('iPhoneX', 1335, 640, 1.0),
        packItem('iPad', 960, 720, 1.0),
    ]
    plist.resolutions = items
    writePlist(plist, xml_path, binary=False)
    print '完成'

# 遍历文件夹
def getFile(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                # find dir todo ..
                if item in DirExt:
                    # not in DirExt
                    continue

                getFile(full_path)

            file_ext = item.split(".")[-1]
            if file_ext not in FileExt:
                # not in FileExt
                continue

            reset(full_path)
    except Exception, ex:
        print ex  

getFile('/fytx2NewSvn/res/trunk/CCB/Resources/ccbi')