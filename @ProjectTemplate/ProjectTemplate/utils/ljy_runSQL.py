''' 
* @Author: lijiayi  
* @Date: 2019-09-10 14:33:42  
* @Last Modified by:   lijiayi  
* @Last Modified time: 2019-09-10 14:33:42  
'''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

import os,sys
import time
from ljy_ConnDB import ConnectDB
from ljy_config import getconf
from ljy_pgsql import pgsql
import report

class runSQL(pgsql):
    def __init__(self):
        pgsql.__init__(self)
        self.conn=ConnectDB()
        self.sqlstr_file=getconf().getsqllist()
        if self.sqlstr_file == -1:
            self.sqlstr_file=None
        self.log_path=getconf().get_log_path()
        self.conf=getconf()

    def get_saveFile(self,funcname=None):
        saveFile=self.log_path+"%s_result.txt"%(funcname)
        if os.path.exists(saveFile):
            os.remove(saveFile)
        return saveFile

    def logg(self,data=None,funcname=None):
        saveFile=self.get_saveFile(funcname)
        with open(saveFile,"a",encoding='utf-8') as f:
            for i in data:
                f.write(str(i))
        # print("Created>%s!"%(saveFile))

    def get_result(self,sqlstr_list=None):
        result_list=[]
        temp=[]
        if type(sqlstr_list) is not list:
            temp.append(sqlstr_list)
        else:
            temp=sqlstr_list
        # print(temp)
        for i in temp:
            result=self.conn.sqlrun(i)
            nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            result_list.append("["+nowtime+"]: "+i+"\n"+str(result)+"\n-----------------\n")
        return result_list

    # def get_result_withThread(self,sqlstr_list=None):
    #     result_list=[]
    #     temp=[]
    #     if type(sqlstr_list) is not list:
    #         temp.append(sqlstr_list)
    #     else:
    #         temp=sqlstr_list
    #     # print(temp)
    #     import threading
    #     for i in temp:
    #         target=threading.Thread(target=self.conn.sqlrun,args=(i,))
    #         while threading.active_count()>int(self.conf.get_DB_config()["thread"]):
    #             time.sleep(10)
    #         target.start()
    #         result="多线程模式未获取返回值"
    #         nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #         result_list.append("["+nowtime+"]: "+i+"\n"+str(result)+"\n-----------------\n")
    #     return result_list

    def get_result_withThread(self,sqlstr_list=None,saveFile=None):
        result_list=[]
        temp=[]
        if type(sqlstr_list) is not list:
            temp.append(sqlstr_list)
        else:
            temp=sqlstr_list
        # print(temp)
        import threading
        for i in temp:
            target=threading.Thread(target=self.conn.sqlrun_withthread,args=(i,saveFile))
            while threading.active_count()>int(self.conf.get_DB_config()["thread"]):
                time.sleep(10)
            target.start()

    def run_sqlfile(self,sqlstr_list=None):
        funcname=sys._getframe().f_code.co_name
        print("start %s..."%(funcname))
        sqlstr_list=self.sqlstr_file
        if sqlstr_list is None:
            return -1
        result_list=self.get_result(sqlstr_list)
        self.logg(data=result_list,funcname=funcname)
        return 0

    def template(self):
        sqlstr_list=self.SQL_temp_t_e_vote_title_desc()
        funcname=sys._getframe().f_code.co_name
        print("start %s..."%(funcname))
        try:
            self.get_result_withThread(sqlstr_list,self.get_saveFile(funcname))
            # self.logg(data=result_list,funcname=funcname)
        except Exception as e:
            return e
        return 0

    def app_d_js_jbxxdbtj(self):
        sqlstr_list=self.SQL_app_d_js_jbxxdbtj()
        funcname=sys._getframe().f_code.co_name
        print("start %s..."%(funcname))
        try:
            self.get_result_withThread(sqlstr_list,self.get_saveFile(funcname))
            # self.logg(data=result_list,funcname=funcname)
        except Exception as e:
            return e
        return 0

    def app_d_xs_xsgsxx(self):
        sqlstr_list=self.SQL_app_d_xs_xsgsxx()
        funcname=sys._getframe().f_code.co_name
        print("start %s..."%(funcname))
        try:
            self.get_result_withThread(sqlstr_list,self.get_saveFile(funcname))
            # self.logg(data=result_list,funcname=funcname)
        except Exception as e:
            return e
        return 0

    def DBquit(self):
        self.conn.DBquit()

    def main(self):
        # if self.app_d_js_jbxxdbtj() == 0:
        #     print("pass\n")
        # else:
        #     print(-1)
        if self.app_d_xs_xsgsxx() == 0:
            print("pass\n")
        else:
            print(-1)

# class Mythread(threading.Thread):
#     def __init__(self,func,args):
#         Thread.__init__(self):
#         self.func=func
#         self.args=args
    
#     def run(self):
#         result=self.func(self.args)


def getReportBody(caseName=None,caseStatus=None,caseCount=None):
    return report.getRowStr(caseUrl="/",caseId="SQLscript",caseName=caseName,caseStatus=caseStatus,caseCount=caseCount)

def getReportHtml(reportBody=None):
    return report.getHtmlStr(projecName='-',totalCase="-",passCase="-",failCase="-",start="-",end="-",totalRowStr=reportBody)


if __name__=='__main__':
    r=runSQL()
    result=None
    if r.run_sqlfile() == -1:
        print("No sqlfile.\n")
        result=False
    else:
        print("pass\n")
        result=True
    # r.main()
    r.DBquit()

    reportBody=''
    reportBody=getReportBody(caseName="run_sqlfile",caseStatus=result,caseCount=10)
    reportHtml = getReportHtml(reportBody)
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\"+"Result.Html", 'w',encoding='utf-8') as f:
        f.write(reportHtml)
