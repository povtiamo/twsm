#!/usr/python
# coding=utf-8
import os, time, hashlib, json, codecs, sys

# 临时文件存放位置
APK_PATH  = sys.argv[1]

# SAVE_JSON_PATH = os.path.dirname(APK_PATH)
SAVE_JSON_PATH = APK_PATH
TEMP_PATH = "%s/tmp_%s_old" % (SAVE_JSON_PATH, int(time.time()))
KEY_PATH = "%s/assets/res" % TEMP_PATH

# 需要检查的格式
FileExt = ['DS_Store']
# 不需要抽查的文件夹
DirExt = []
file_md5_map = {}

old_arr = []

# 获取MD5
def get_md5(path):
    fd = open(path,'rb')
    md5=hashlib.md5(fd.read()).hexdigest()
    fd.close()
    return md5

# 
def saveFileMD5(path):
    key = os.path.relpath(path, KEY_PATH)
    file_md5_map[key]=get_md5(path)

# 遍历文件夹
def getFile(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                getFile(full_path)
            else:
                file_ext = item.split(".")[-1]
                if file_ext in FileExt:
                    # not in FileExt
                    continue
                saveFileMD5(full_path)
    except Exception, ex:
        print ex

def init(apkPath):
    global old_arr

    print apkPath
    os.mkdir(TEMP_PATH)
    # 解压
    os.system("unzip %s -d %s" % (apkPath, TEMP_PATH))
    # 刪除ServerConfig.json
    os.system("rm -rf %s/assets/res/ServerConfig.json" % TEMP_PATH)

    #获取旧版本号
    tmp_fd  = open("%s/assets/res/ver.txt" % TEMP_PATH)
    old_ver = tmp_fd.read()
    old_arr = old_ver.split(".")
    tmp_fd.close()

    # src移动到res里面
    os.system("mv %s/assets/src %s/assets/res" % (TEMP_PATH, TEMP_PATH))


def cleanUp():
    path = "%s/md5"%(SAVE_JSON_PATH)
    print path

    if not os.path.exists(path):
        os.makedirs(path)
    
    downloadFileListPath = "%s/%s.json"%(path, old_arr[2])
    json.dump(obj=file_md5_map,fp=codecs.open(downloadFileListPath , "w", encoding="utf-8"), indent=2, sort_keys=True, ensure_ascii=False, encoding='utf-8')
    os.system("rm -rf %s" % TEMP_PATH)

def main(apk_path):
    global file_md5_map
    print apk_path
    init(apk_path)
    getFile("%s/assets/res"%(TEMP_PATH))
    cleanUp()
    file_md5_map = {}
    print file_md5_map


for item in os.listdir(APK_PATH):
    full_path = os.path.join(APK_PATH, item)
    if not os.path.isdir(full_path):
        file_ext = item.split(".")[-1]
        if file_ext in FileExt:
            # not in FileExt
            continue
        main(full_path)
