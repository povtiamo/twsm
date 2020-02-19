#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

import ljy_base
import json

AppID=16600152
API_Key="oNnWciQupqWPH871GU0T77dy"
Secret_Key="xMNjsEhc1RbIxGlhWdX9ACDe5LjktDHi"
headers={
"Accept":"application/json, text/plain, */*",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Content-Type":"application/json;charset=UTF-8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9"
}

uri="https://aip.baidubce.com/oauth/2.0/token"
params={
"grant_type":"client_credentials",#写死client_credentials
"client_id":API_Key,#API Key
"client_secret":Secret_Key#Secret Key
}
params=ljy_base.base()._urlencode(params)
result=ljy_base.base().postHTTP(uri=uri,params=params,headers=headers)
result=json.loads(result.text)
access_token=result["access_token"]
# print(result["access_token"])


#uri="https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
# uri="https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"#通用
uri="https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"#高精度
# uri="https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"

params={
"access_token":access_token
}
params=ljy_base.base()._urlencode(params)

# file_path="C:\\Users\\povti\\Desktop\\test\\test5.jpg"
file_path="C:\\Users\\povti\\Desktop\\baoke.png"
# file_path="C:\\Users\\povti\\Desktop\\测试文档\\20180828150524307.jpg"

f_b64=ljy_base.base().file_To_Base64(file_path)
image_data=ljy_base.base()._urlencode(f_b64)

data={"image":f_b64}
result=ljy_base.base().postHTTP(uri=uri,params=params,data=data,headers=None)#直接json格式发过去
result=json.loads(result.text)
# print(result)

content=""
for temp in result["words_result"]:
	content+="%s\n"%(temp["words"])
# 去除数字以外的其他字符
fil = filter(lambda x:x.isalpha() or x.isdigit(), content)#isalpha是否英语，isdigit是否数字
fil =filter(None,content)
new_text = ''
for i in fil:
	new_text += i
print(new_text)
