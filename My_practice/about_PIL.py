from PIL import Image
import hashlib


file_path = "D:\\性能测试\\file_IO\\test_3.jpg"

def getFileMD5(file_path):
    with open(file_path,"rb") as file:
        filemd5=hashlib.md5(file.read()).hexdigest()#get 32 value
    return filemd5


md5=getFileMD5(file_path)
print("before:%s"%(md5))
img = Image.open(file_path)
img.save(file_path, quality=95)
md5=getFileMD5(file_path)
print("after:%s"%(md5))