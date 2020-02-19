''' 
* @Author: lijiayi  
* @Date: 2019-09-16 17:51:35  
* @Last Modified by:   lijiayi  
* @Last Modified time: 2019-09-16 17:51:35  
'''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

'''
普通小学802所，
在校生492106人，
专任教师26137人，
每名专任教师覆盖在校生19人，

普通中学189所，
在校生243675人，
专任教师17771人，
每名专任教师覆盖在校生14人，

高等学校18所，
在校生148567人，
专任教师7840人，
每名专任教师覆盖在校生19人
'''

from ljy_config import getconf

class pgsql(object):
    def __init__(self):
        self.conf=getconf()

    # temp_t_e_vote_title_desc
    def SQL_template(self):
        conf=self.conf.get_table_config("temp_t_e_vote_title_desc")
        sqlstr_list=[]
        for i in range(int(conf["loop"])):
            values_list=conf["values"].replace("%s","%03d"%(i))
            sqlstr=u"""INSERT INTO {tables}({columns}) VALUES({values});"""
            sqlstr=sqlstr.format(
                columns=conf["columns"],
                tables=conf["tables"],
                values=values_list
            )
            # print(sqlstr)
            sqlstr_list.append(sqlstr)
        return sqlstr_list

    # app_d_js_jbxxdbtj
    def SQL_app_d_js_jbxxdbtj(self):
        conf=self.conf.get_table_config("app_d_js_jbxxdbtj")
        sqlstr_list=[]
        for i in range(int(conf["loop"])):
            values_list=conf["values"].replace("%s","%d"%(i+1))
            sqlstr=u"""INSERT INTO {tables}({columns}) VALUES({values});"""
            sqlstr=sqlstr.format(
                columns=conf["columns"],
                tables=conf["tables"],
                values=values_list
            )
            # print(sqlstr)
            sqlstr_list.append(sqlstr)
        return sqlstr_list

    # app_d_xs_xsgsxx
    def SQL_app_d_xs_xsgsxx(self):
        conf=self.conf.get_table_config("app_d_xs_xsgsxx")
        sqlstr_list=[]
        for i in range(int(conf["loop"])):
            values_list=conf["values"].replace("%s","%d"%(i+1))
            sqlstr=u"""INSERT INTO {tables}({columns}) VALUES({values});"""
            sqlstr=sqlstr.format(
                columns=conf["columns"],
                tables=conf["tables"],
                values=values_list
            )
            # print(sqlstr)
            sqlstr_list.append(sqlstr)
        return sqlstr_list

if __name__=='__main__':
    p=pgsql()
    print(p.SQL_app_d_js_jbxxdbtj())