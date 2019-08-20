#!/usr/python
# coding=utf-8
import os, time, hashlib, json, codecs, sys, shutil

# 临时文件存放位置
SAVE_JSON_PATH  = sys.argv[1]

# 需要过滤的文件
FileExt = ['DS_Store']

# 循环对比
def compareAll(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            print full_path
            if not os.path.isdir(full_path):
                compareOne(full_path)
    except Exception, ex:
        print ex

# 对比
def compareOne(md5File): 
    strarr = os.path.splitext(md5File) 
    if strarr[1] != ".json":
        return

    print "compare : " + md5File
    ver_name = os.path.basename(md5File).split(".")[0]
    print "ver : " + ver_name
    need_packet_files = []
    new_file_md5_map = []
    old_file_md5_map = []

    md5Path = "%s/new"%(SAVE_JSON_PATH)
    new_file_md5_map = readOldVerMd5Json("%s/%s"%(md5Path, os.path.basename(md5File)))
    old_file_md5_map = readOldVerMd5Json(md5File)
    for fileKey in new_file_md5_map:
        # print fileKey
        file_ext = fileKey.split(".")[-1]
        if file_ext in FileExt:
            # not in FileExt
            continue

        # old_md5 = old_file_md5_map[fileKey]
        old_md5 = old_file_md5_map.get(fileKey)
        # print 'old_md5 = ' , old_md5
        if not old_md5 :
            # 旧包里面不存在就是用需要更新
            need_packet_files.append(fileKey)
            continue

        new_md5 = new_file_md5_map[fileKey]
        # print 'new_md5 = ' , new_md5
        if old_md5 != new_md5:
            # md5不一样
            need_packet_files.append(fileKey)
            continue

    # print '需要打包的文件数：', need_packet_files.size()
    # 打包压缩
    downloadFileListPath = "%s/%s.json"%(SAVE_JSON_PATH, ver_name)
    json.dump(obj=need_packet_files,fp=codecs.open(downloadFileListPath , "w", encoding="utf-8"), indent=2, sort_keys=True, ensure_ascii=False, encoding='utf-8')
    
# 对比
def readOldVerMd5Json(md5File): 
    tmp_fd  = open(md5File)
    json_file = tmp_fd.read()
    tmp_fd.close()
    data = json.loads(json_file)
    newData = {}
    for x in data:
        newData[x]=x
    return newData

def main():
    md5Path = "%s/old"%(SAVE_JSON_PATH)
    if os.path.exists(md5Path):
        compareAll(md5Path)

main()