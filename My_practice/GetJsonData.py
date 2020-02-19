#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

import os,sys,json,traceback

def FormatJson(Data):
    try:
        Data_json=json.loads(Data)
    except:
        ex = Exception("Data Read error！\n%s"%(Data))
        raise ex
    return Data_json

def ReadFile(path):
    if os.path.exists(path):
        try:
            with open("%s"%(path),"r") as f:
                f_read=f.read().replace("\n","").replace("\t","").replace(" ","")
                f_json=FormatJson(f_read)
                return f_json
        except:
            ex = Exception("File Read error! %s"%(path))
    else:
        print("%s Not Found!"%(path))

if __name__ == "__main__":
    path="D:\\Python\\My_practice\\json.txt"
    DataJson=ReadFile(path)
    questionList=DataJson["paperAnswer"]["questionList"]
    # questionId=[]
    # typeLevel=[]
    questionId=""
    typeLevel=""
    for i in questionList:
        # questionId.append(i["questionId"])
        # typeLevel.append(i["typeLevel"])
        questionId+="%s,"%(i["questionId"])
        typeLevel+="%s,"%(i["typeLevel"])

    print("examId:%s\n"%(DataJson["examId"]))
    print("orgId:%s\n"%(DataJson["orgId"]))
    print("publishId:%s\n"%(DataJson["publishId"]))
    print("snapshot:%s\n"%(DataJson["paperAnswer"]["snapshot"]))
    print("questionId:%s\n"%(questionId))
    print("typeLevel:%s\n"%(typeLevel))
    print("lefttop:%s,%s\n"%(DataJson["paperAnswer"]["totalLeft"],DataJson["paperAnswer"]["totalTop"]))