#!/usr/python
# coding=utf-8
import os, time, hashlib, json, codecs, sys, shutil

# 临时文件存放位置
ZIP_PATH  = sys.argv[1]
APK_PATH  = sys.argv[2]

SAVE_JSON_PATH = ZIP_PATH
TEMP_PATH = "%s/tmp_%s_old" % (SAVE_JSON_PATH, int(time.time()))
KEY_PATH = "%s/assets/res" % TEMP_PATH

new_file_md5_map = {}
need_packet_files = []
new_arr = ''

# 需要过滤的文件
FileExt = ['DS_Store']

# 循环对比
def compareAll(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
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
    # packZip(ver_name, need_packet_files)
    downloadFileListPath = "%s/%s.json"%(SAVE_JSON_PATH, ver_name)
    json.dump(obj=need_packet_files,fp=codecs.open(downloadFileListPath , "w", encoding="utf-8"), indent=2, sort_keys=True, ensure_ascii=False, encoding='utf-8')
    

def packZip(ver, files):
    save_path = "%s/zip/%s/%s"%(ZIP_PATH, new_arr, ver)
    print save_path
    os.makedirs(save_path)
    # print '需要打包的文件2', files
    # shellFiles = ' '.join(files)
    # print "cd %s; zip -r %s/%s.zip %s" % (KEY_PATH, save_path, ver, shellFiles)
    # os.system("cd %s; zip -r %s/%s.zip %s" % (KEY_PATH, save_path, ver, shellFiles))
    for name in files:
        src = '%s/%s'%(KEY_PATH, name)
        dst = '%s/%s'%(save_path, name) 
        copy_file(src, dst)

    file_list = os.popen("ls %s" % save_path).read()
    file_list = file_list.split("\n")
    new_file_list = []
    for _f in file_list:
        if -1 == _f.find("md5.txt") and -1 == _f.find("package.zip"):
            new_file_list.append(_f)
    file_list = " ".join(new_file_list)

    #压缩包
    zip_file_name = '%s/20001_package.zip' % (save_path)

    if os.path.exists(zip_file_name):
        os.system("rm -rf %s" % zip_file_name)

    os.system("cd %s; zip -r %s %s" % (save_path, zip_file_name, file_list))
    os.system("cd %s; rm -rf %s" % (save_path, file_list))


# 拷贝文件
def copy_file(src,dst):
    dirname = os.path.dirname(dst)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    shutil.copy(src,dst)

# 获取MD5
def get_md5(path):
    fd = open(path,'rb')
    md5=hashlib.md5(fd.read()).hexdigest()
    fd.close()
    return md5

# 对比
def readOldVerMd5Json(md5File): 
    tmp_fd  = open(md5File)
    json_file = tmp_fd.read()
    tmp_fd.close()
    data = json.loads(json_file)
    return data

# 记录文件MD5
def saveFileMD5(path):
    key = os.path.relpath(path, KEY_PATH)
    new_file_md5_map[key]=get_md5(path)

# 遍历文件夹
def getFile(path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                getFile(full_path)
            else:
                saveFileMD5(full_path)
    except Exception, ex:
        print ex

def init(apkPath):
    global new_arr
    os.mkdir(TEMP_PATH)
    # 解压
    print "unzip -q %s -d %s" % (apkPath, TEMP_PATH)
    os.system("unzip -q %s -d %s" % (apkPath, TEMP_PATH))
    # 刪除ServerConfig.json
    os.system("rm -rf %s/assets/res/ServerConfig.json" % TEMP_PATH)
    # src移动到res里面
    os.system("mv %s/assets/src %s/assets/res" % (TEMP_PATH, TEMP_PATH))

    # os.mkdir("%s/assets/res/ccbResources" % TEMP_PATH)
    # 加入隐藏文件
    os.system("touch %s/assets/res/ccbResources/.nomedia" % TEMP_PATH)

    #获取旧版本号
    tmp_fd  = open("%s/assets/res/ver.txt" % TEMP_PATH)
    new_ver = tmp_fd.read()
    new_arr = new_ver.split(".")[-1]
    print new_arr
    tmp_fd.close()

def cleanUp():
    os.system("rm -rf %s" % TEMP_PATH)

    downloadFileListPath = "%s/%s.json"%(SAVE_JSON_PATH, new_arr)
    json.dump(obj=new_file_md5_map,fp=codecs.open(downloadFileListPath , "w", encoding="utf-8"), indent=2, sort_keys=True, ensure_ascii=False, encoding='utf-8')

def main():
    init(APK_PATH)
    getFile("%s/assets/res"%(TEMP_PATH))

    md5Path = "%s/md5"%(SAVE_JSON_PATH)
    if os.path.exists(md5Path):
        compareAll(md5Path)

    cleanUp()

main()