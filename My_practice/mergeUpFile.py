#!/usr/python
# coding=utf-8
import os, time, hashlib, json, codecs, sys, shutil, random

# 临时文件存放位置
save_path  = sys.argv[1]

# 需要合并的更新文件
need_merge_files = []

save_data = {}
# 需要检查的格式
FileExt = ['DS_Store']

# 合并
def mergeFile(path): 
    print path
    global save_data
    file_data = readJson(path)

    if len(save_data) < 1:
        for item in file_data:
            file_md5 = file_data.get(item)
            save_data[item] = file_md5
    else:
        for item in file_data:
            # 文件里的md5
            file_md5 = file_data.get(item)
            # 目前保存
            data_md5 = save_data.get(item)

            if data_md5 == None:
                # 如果旧的没有也是必须要更新
                md5 = 'empty'
                for x in xrange(1,27):
                    md5 = md5+str(random.randrange(0,9))
                save_data[item]=md5
            elif file_md5 != data_md5:
                # 如果不相等就随机一个md5，保证更新下载
                md5 = 'mergre'
                for x in xrange(1,26):
                    md5 = md5+str(random.randrange(0,9))
                save_data[item]=md5

# 读取
def readJson(path): 
    tmp_fd  = open(path)
    json_file = tmp_fd.read()
    tmp_fd.close()
    data = json.loads(json_file)

    print '===', path
    print data

    return data

# 保存
def saveJson(path): 
    json.dump(obj=save_data,fp=codecs.open(path , "w", encoding="utf-8"), indent=2, sort_keys=True, ensure_ascii=False, encoding='utf-8')

# 遍历文件夹
def getFile(path):
    global need_merge_files

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
                # saveFileMD5(full_path)
                need_merge_files.append(full_path)
    except Exception, ex:
        print ex

def main():
    getFile(save_path)
    for file_path in need_merge_files:
        mergeFile(file_path)
    saveJson('%s/new.json'%(save_path))

main()