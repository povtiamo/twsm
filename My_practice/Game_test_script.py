#!/usr/bin/python
#-*-coding:utf-8-*-

import urllib
import urllib2
import json
import socket
import ctypes
import struct
import binascii
import threading
import time
import random
import traceback
import sys
import os
import threading
import logging
import httplib

os.chdir(os.path.dirname(sys.argv[0]))
##decode的作用是将其他编码的字符串转换成unicode编码，如str1.decode('gb2312')，表示将gb2312编码的字符串str1转换成unicode编码。
##encode的作用是将unicode编码转换成其他编码的字符串，如str2.encode('gb2312')，表示将unicode编码的字符串str2转换成gb2312编码。
# pdb debug switch
# _DEBUG = True
_DEBUG = False
if _DEBUG is True:
    import pdb
    pdb.set_trace()



class Client():
    #account url
    URL = "http://10.17.172.222:8081/"
    # URL = "http://fy2server.fytxonline.com"

    for i in range(11):
        choose_ID=input("select a SERVER_ID (1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19,3000,3002,23,30) >>")
        choose_ID=int(choose_ID)
        if i < 10:
            if choose_ID in [6,7] or choose_ID not in range(1,3100):
                print "False Enter!"
                continue
            else:
                break
        else:
            print "what are u doing???"
            sys.exit()

    SERVER_ADDR_index={
        1:("10.21.210.210",2001),
        2:("10.21.210.210",2002),
        3:("10.21.210.210",2003),
        4:("10.21.210.210",2004),
        5:("10.21.210.210",2005),
        8:("10.21.210.189",2001),
        9:("10.21.210.189",2002),
        10:("10.21.210.189",2003),
        11:("10.21.210.189",2004),
        12:("10.21.210.189",2005),
        13:("10.21.210.189",2006),
        14:("10.21.210.189",2007),
        15:("10.21.210.189",2008),
        16:("10.17.172.221",2001),
        17:("10.17.172.221",2002),
        18:("10.17.172.221",2003),
        19:("10.17.172.221",2004),
        3000:("10.17.172.222",2003),
        3002:("10.17.172.222",2005),
        23:("10.17.172.222",2007),
        30:("10.17.172.221",2005)
    }
    GM_URL_index={
        1:"http://10.21.210.210:2081",
        2:"http://10.21.210.210:2082",
        3:"http://10.21.210.210:2083",
        4:"http://10.21.210.210:2084",
        5:"http://10.21.210.210:2085",
        8:"http://10.21.210.189:2081",
        9:"http://10.21.210.189:2082",
        10:"http://10.21.210.189:2083",
        11:"http://10.21.210.189:2084",
        12:"http://10.21.210.189:2085",
        13:"http://10.21.210.189:2086",
        14:"http://10.21.210.189:2087",
        15:"http://10.21.210.189:2088",
        16:"http://10.17.172.221:2081",
        17:"http://10.17.172.221:2082",
        18:"http://10.17.172.221:2083",
        19:"http://10.17.172.221:2084",
        3000:"http://10.17.172.222:2083",
        3002:"http://10.17.172.222:2085",
        23:"http://10.17.172.222:2087",
        30:"http://10.17.172.221:2085"
    }

    SERVER_ADDR=SERVER_ADDR_index[choose_ID]
    GM_URL=GM_URL_index[choose_ID]
    SERVER_ID=int(choose_ID)
    print "SERVER_ADDR:%s ,GM_URL:%s ,SERVER_ID:%s" %(SERVER_ADDR ,GM_URL ,SERVER_ID)

    CONVERT_LIB = ctypes.cdll.LoadLibrary("./pycall.dylib")
    MSG_BASE = struct.Struct("=H i i q")
    MSG_BASE_LEN = 18
    LOGIN_REQ = 12


    # init
    def __init__(self,username,password,times,count):
        self.__username = username
        self.__password = password
        self.__player_id = 0
        self.__net_id = 0
        self.__protocol = 0
        self.__times = times
        self.__count = count
        self.__left_msg=""


    def __del__(self):
        print "-- close socket --"
        if (self.__socket):
            self.__socket.close()

    def register(self):
        data = urllib.urlencode({"username": self.__username,"password": self.__password})
        url = Client.URL + "/client/register"
        print "register:",url,data
        req = urllib2.Request(url,data)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print res

    def login(self):
        if _DEBUG is True:
            import pdb
            pdb.set_trace()
        data = urllib.urlencode({"username": self.__username,"password": self.__password})
        url = Client.URL + "/client/login"
        req = urllib2.Request(url,data)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print res
        # json_data = json.JSONDecoder().decode(res)
        json_data = json.loads(res)
        if (json_data["result"] != 0):
            return
        self.__connect()
        self.__login_account(json_data)
        self.__login_req()
        self.__create_role()
        time.sleep(2)
        # self.heartbeat()
        self.gm_modify_level(9999999,9999999)
        self.gm_modify_man()
        # self.gm_modify_item()
        #self.item_qianghua()
        #self.item_equip()
        self.gm_map()
        #self.join_country()
        self.gm_modify_resource("[10000000,0,10000000,10000000,10000000,10000000,10000000,0,0,0,0,0,0,0,0,0]")
        # self.maoyi()
        #self.touxiang()
        # self.maoyi_move()
        # self.chat_send("国际米兰")
        # self.join_legion(20971546)
        # self.gm_manlevel()
        # self.yaoqianshu()
        # self.huangdi_war_join()
        # self.join_Server_war()
        # self.ob_Server_war()
        self.buzhen()
        #self.kingdom_building()
        # self.biwu_move()
        # self.biwu_sign()
        # self.biwu_enter()
        # self.niangjiu()
        # self.battle_danmu()
        # self.eight_array_enter_city()
        # self.kingdom_hegemony()
        # self.Server_chat(10485762,10485787)
        # self.flower_Server_war(1061158914)
        # self.Server_plunder_buzhen()
        # self.Server_plunder_mianzhan()
        # self.Server_peakwar_sign()
        # for n in range(99):
        #     self.teamwar_create(2)
        #     time.sleep(5)
        # self.keju_init()
        # self.keju_join()
        # self.dianshi_join()
        # self.gm_modify_hougong()
        # self.hougong()
        # self.worldboss_init()
        # self.worldboss_attack()
        # self.CampWar_join()
        # for i in range(35):
        #     self.keju_Question()
        #     self.keju_Answer(1)
            # self.dianshi_Question()
            # self.dianshi_Answer(1)
        self.__del__()



    def join_country(self):
        print "player_times:",self.__times
        country_parse = self.__count
        if self.__times < country_parse/3:
            self.send(2000,"[0]")
            #self.recv()
        elif self.__times < country_parse - country_parse/3 and self.__times >= country_parse/3:
            self.send(2000,"[1]")
            #self.recv()
        else:
            self.send(2000,"[2]")
            #self.recv()

        # self.send(2000,"[1]")
        #self.recv()



    def http_post(self,url, data='', data_type = 'x-www-form-urlencoded',user_agent='', timeout_param=5,timeout=5,headers=[],cookie=''):
        res = None
        urlInfo = httplib.urlsplit(url)
        uri = ( '%s?%s' % (urlInfo.path,urlInfo.query) ) if urlInfo.query else urlInfo.path
        if url.find('https://')>-1:
            conn = httplib.HTTPSConnection(urlInfo.netloc,timeout=timeout or timeout_param)
        else:
            conn = httplib.HTTPConnection(urlInfo.netloc,timeout=timeout or timeout_param)
        try:
            conn.connect()
            
            if data:
                if isinstance(data,unicode):
                    data = data.encode('utf-8')
                conn.putrequest("POST", uri)
            else:
                conn.putrequest("GET", uri)
                
            for k,v in headers:
                conn.putheader(k, v)
                
            if cookie :
                if isinstance(cookie,dict):
                    cookie = ' '.join(['%s=%s;' % (urllib2.quote(str(k)),urllib2.quote(str(v))) for k,v in cookie.iteritems()])
                conn.putheader("Cookie", cookie)
                
            conn.putheader("Content-Length", len(data))
            conn.putheader("Content-Type", "application/%s" % data_type)
            if user_agent!='':
                conn.putheader("User-Agent",user_agent)
                    
            conn.putheader("Connection", "close")
            conn.endheaders()

            if data:
                conn.send(data)

            response = conn.getresponse()
            if response:
                res = response.read()
                response.close()
            
            return res
        
        except socket.timeout:
            raise HttpTimeOut('Connect %s time out' % url)
        except Exception, ex:
            raise ex
        
        conn.close()


    def gm_http_result(self,req_type,content):
        post_data = 'req_type=%d&content=%s' % (req_type, content)
        post_data += ''.join(['&player_id=%s' % str(self.__player_id)])
        post_data = post_data.encode('utf-8')        
        # print "post_data:",post_data
        url = Client.GM_URL + "/service?"

        res=self.http_post(url,data=post_data,timeout=10)
        _r=json.loads(res)
        return _r["msg"]


    def gm_modify_level(self,player_lv,vip_exp):
        if (self.__player_id == 0):
            return
        req_type=1109
        content = [self.__username,player_lv,vip_exp]
        content = json.dumps({"msg": content}, ensure_ascii=False)
        print content
        print "gm_level_sending...:"
        result=self.gm_http_result(req_type,content)
        print "result:",result

    def gm_modify_resource(self,resource):
        if (self.__player_id == 0):
            return
        content = "{\"msg\":"
        content += resource
        content += "}"
        # msg = urllib.urlencode({"req_type": "1110","content": content,"player_id": self.__player_id})
        # url = Client.GM_URL + "/service?"
        # req = urllib2.Request(url,msg)
        # print "gm_resource_sending..."
        # res_data = urllib2.urlopen(req)
        # res = res_data.read()
        # print "gm_resource_result:",res

        req_type = 1110
        # content = resource
        # content = json.dumps({"msg": content}, ensure_ascii=False)
        # print content
        print "gm_resource_sending..."
        result=self.gm_http_result(req_type,content)
        print "result:",result

    def gm_modify_man(self):
        with open("./gm_manlist.txt","r") as f:
            list_read = f.read()
            list = list_read.split(",")
            gm_list = []
            print "gm_man_sending..."
            for i in list:
                last = False
                if list.index(i) + 1 == len(list):
                    gm_list.append(str(i))
                    last = True
                    pass
                if len(gm_list) == 30 or last is True:
                    post_list = ",".join(gm_list)
                    content = "{\"msg\":["
                    content += str(post_list)
                    content += "]}"
                    # msg = urllib.urlencode({"req_type": "1116","content": content,"player_id": self.__player_id})
                    # url = Client.GM_URL + "/service?"
                    # req = urllib2.Request(url,msg)
                    # res_data = urllib2.urlopen(req)
                    # res = res_data.read().decode('utf-8')

                    req_type = 1116
                    # content = post_list
                    # content = json.dumps({"msg": content}, ensure_ascii=False)
                    # print content
                    result=self.gm_http_result(req_type,content)
                    print "result:",result

                    gm_list = []
                    if not i:
                        pass
                    else:
                        gm_list.append(str(i))
                elif len(gm_list) < 30:
                    gm_list.append(str(i))
                else:
                    pass

    def gm_manlevel(self):
        print "gm_man_level_sending..."
        with open("./gm_manlist.txt","r") as f:
            list_read = f.read()
            list_read = list_read.split(",")
            gm_list = []
            print "gm_man_sending..."
            for i in list_read:
                list = [int(i),99999999]
                last = False
                if list_read.index(i) + 1 == len(list_read):
                    gm_list.append(list)
                    last = True
                    pass
                if len(gm_list) == 30 or last is True:
                    content = "{\"msg\":"
                    content += str(gm_list)
                    content += "}"
                    # msg = urllib.urlencode({"req_type": "1113","content": content,"player_id": self.__player_id})
                    # url = Client.GM_URL + "/service?"
                    # req = urllib2.Request(url,msg)
                    # res_data = urllib2.urlopen(req)
                    # res = res_data.read()

                    req_type = 1113
                    # content = gm_list
                    # content = json.dumps({"msg": content}, ensure_ascii=False)
                    # print content
                    result=self.gm_http_result(req_type,content)
                    print "result:",result

                    gm_list = []
                    if not i:
                        pass
                    else:
                        gm_list.append(list)
                elif len(gm_list) < 30:
                    gm_list.append(list)
                else:
                    pass

    def gm_map(self):
        with open("./gm_map_list.txt","r") as f:
            gm_map_list = f.read()
            json_gm_map_list = json.JSONDecoder().decode(gm_map_list)
            gm_list = []
            print "gm_map_sending..."
        for i in json_gm_map_list:
            last = False
            if json_gm_map_list.index(i)+1 == len(json_gm_map_list):
                gm_list.append(i)
                last = True
                pass
            if len(gm_list) == 50 or last is True:
                content = "{\"msg\":"
                content += str(gm_list)
                content += "}"
                # msg = urllib.urlencode({"req_type": "1122","content": content,"player_id": self.__player_id})
                # url = Client.GM_URL + "/service?"
                # req = urllib2.Request(url,msg)
                # res_data = urllib2.urlopen(req)
                # res = res_data.read().decode('utf-8')

                req_type = 1122
                # content = gm_list
                # content = json.dumps({"msg": content}, ensure_ascii=False)
                # print content
                result=self.gm_http_result(req_type,content)
                print "result:",result

                gm_list = []
                if not i:
                    pass
                else:
                    gm_list.append(i)
            elif len(gm_list) < 50:
                gm_list.append(i)
            else:
                pass

    def gm_modify_item(self):
        if (self.__player_id == 0):
            return
        #item_list = [9500,9501,9502,9503,9504,9505,9506,9507,9508]
        with open("./gm_itemlist.txt","r")as f:
			item_list=f.read().split(",")

        gm_list = []
        item_times=10
        print "gm_item_sending..."
        for i in item_list:
            last = False
            # list = [i,999]
            list = [int(i),int(item_times)]
            if item_list.index(i) + 1 == len(item_list):
                gm_list.append(list)
                last = True
                pass
            if len(gm_list) == 30 or last is True:
                content = "{\"msg\":"
                content += str(gm_list)
                content += "}"
                # msg = urllib.urlencode({"req_type": "1117","content": content,"player_id": self.__player_id})
                # url = Client.GM_URL + "/service?"
                # req = urllib2.Request(url,msg)
                # res_data = urllib2.urlopen(req)
                # res = res_data.read().decode('utf-8')

                req_type = 1117
                # content = gm_list
                # content = json.dumps({"msg": content}, ensure_ascii=False)
                # print content
                result=self.gm_http_result(req_type,content)
                print "result:",result

                gm_list = []
                if not i:
                    pass
                else:
                    gm_list.append(list)
            elif len(gm_list) < 30:
                gm_list.append(list)
            else:
                pass



    def heartbeat(self):
        self.send(301,"[]")
        #self.recv()

    def chat_send(self,talk_key):
        msg = "[0,"
        msg += "{\"w\":\""
        msg += self.__username
        msg += str(talk_key)
        msg += "\"},[\"\"]]"
        # 发送空字符
        # self.send(1750,"[]")
        #正常发送
        # self.send(1750,msg)
        #晚宴
        msg = "[5,{\"c\":0,\"w\":\"" + str(talk_key) + "\"},[\"\"]]"
        self.send(3003,"[]")
        self.send(1550,"[]")
        self.send(2403,"[]")
        self.send(1750,msg)
        # self.recv()

    def join_legion(self,legion_id):
        print "join legion:%s"%(legion_id)
        self.send(1500,"[1,9999]")
        self.send(1508,"[false,%s]"%(legion_id))
        self.send(1502,"[]")
        self.send(1503,"[]")

    def touxiang(self):
        self.send(1306,"[2176]")

    def kingdom_building(self):
        msg="[0]"
        self.send(2664,msg)
        msg="[1,1]"
        self.send(2002,msg)
        # self.recv()



    def maoyi(self):
        self.send(1809,"[]")
        #self.recv()

    def maoyi_move(self):
        this = [8,54]
        target = [8,54]
        msg = "["
        msg += str(this) + "," + str(target)
        msg += "]"
        self.send(1805,msg)
        #self.recv()

    def item_qianghua(self):
        item_ID=9500001
        msg="["+str(item_ID)+",10]"
        self.send(1404,msg)
        #self.recv()
        item_ID=9500002
        msg="["+str(item_ID)+",10]"
        self.send(1404,msg)
        #self.recv()

    def item_equip(self):
        item_ID = 9500001
        msg = "[127,[" + str(item_ID) + "]]"
        self.send(1356,msg)
        #self.recv()
        item_ID = 9500002
        msg = "[227,[" + str(item_ID) + "]]"
        self.send(1356,msg)
        #self.recv()


    def join_Server_war(self):
        self.send(21304,"[]")
        #self.recv()

    def rank_Server_war(self):
        pass

    def basic_Server_war(self):
        pass

    def flower_Server_war(self,flower_id):
        player_id = "[" + str(flower_id) + "]"
        self.send(21308,player_id)

    def ob_Server_war(self):
        #join_ob
        player_id = "[" + str(self.__player_id) + "]"
        # player_id = "[" + str(1060110337) + "]"
        self.send(21307,player_id)
        # self.recv()
        player_id = "[" + str(self.__player_id) + "]"
        self.send(21309,player_id)
        # self.recv()

    def buzhen(self):
        with open("./gm_manlist.txt","r") as f:
            list_read = f.read().split(",")
            list_ = []
            for i in list_read:
                list_.append(int(i))
            list_random=random.sample(list_,6)
            msg=[]
            for i in list_random:
                msg.append(int(i))
            print "buzhen:==>%s" %(msg)

        self.send(1468,str(msg))
        # # self.recv()
        # self.send(21305,"[]")
        # # self.recv()
        # self.send(1553,"[8]")
        # #self.recv()
        # msg = "[8,[-1,127,-1,227,3227,327,427,-1,527]]"
        # self.send(1552,msg)
        # #self.recv()

    def biwu_move(self):
        msg="["+str(self.__times)+","+str(self.__times)+"]"
        self.send(4462,msg)
        # self.recv()

    def biwu_sign(self):
        msg = "[8,[-1,127,-1,227,3227,327,427,-1,527]]"
        self.send(4459,msg)
        # self.recv()
        self.send(4458,"[]")
        # self.recv()
        self.send(4464,"[]")
        # self.recv()
        self.send(4454,"[]")
        #self.recv()

    def biwu_enter(self):
        self.send(4450,"[]")
        # self.recv()
        self.send(4452,"[]")
        #self.recv()

    def Server_chat(self,player_A,player_B):
        msg = "[4,{\"pkIds\":[" + str(player_A) +"," +str(player_B) + "],\"color\":{\"r\":138,\"b\":90,\"g\":215},\"w\":\""
        # msg = "[4,{\"color\":{\"r\":138,\"b\":90,\"g\":215},\"w\":\""
        msg += str(self.__username)
        msg += "/42/42当然是原谅它当然是原谅它当然是原谅它当然是原谅它当然是原谅它\"},[\"\"]]"
        self.send(1750,msg)
        #self.recv()

    def teamwar_create(self,team_ID):
        msg =  "[false,20,"
        msg += str(team_ID)
        msg += "]"
        self.send(2100,"[]")
        # self.recv()
        self.send(2105,"[" + str(team_ID) + "]")
        # self.recv()
        self.send(2101,msg)
        # self.recv()

    def keju_init(self):
        msg = "[]"
        self.send(3358,msg)
        self.send(3351,msg)
    
    def keju_join(self):
        msg = "[]"
        self.send(3352,msg)

    def keju_Question(self):
        msg = "[]"
        self.send(3353,msg)

    def keju_Answer(self,no):
        msg = "["+str(no)+"]"
        self.send(3354,msg)

    def dianshi_join(self):
        msg = "[]"
        self.send(3366,msg)

    def dianshi_Question(self):
        msg = "[]"
        self.send(3355,msg)

    def dianshi_Answer(self,no):
        msg = "["+str(no)+"]"
        self.send(3356,msg)

    def wanneng(self,i):
        msg = "[1,9,\""
        msg += str(i)
        msg += "\",1]"
        print msg
        self.send(2625,msg)
        #self.recv()

    def yaoqianshu(self):
        msg = "[10]"
        self.send(3601,msg)
        #self.recv()

    def niangjiu(self):
        # msg = "[0,0,0]"
        msg = "[-1,-1,-1]"
        self.send(3900,msg)
        #self.recv()


    def battle_danmu(self):
        Map_ID = "1009"
        content = "给女装大佬沏茶，cat%s原谅绿" %(self.__times)
        msg = "[" + str(Map_ID) + ",[\"" + str(content) + "\",\"00FA9A\"," + str(self.__player_id) + "]]"
        self.send(3003,"[]")
        self.send(2100,"[]")
        self.send(1522,msg)
        #self.recv()


    def eight_array_enter_city(self):
        #init
        self.send(4404,"[]")
        msg = "{\"startPos\":{\"y\":27,\"x\":93},\"isInCity\":false,\"playerSex\":0,\"playerId\":\"%s\",\"isAction\":true,\"endPos\":{\"y\":27,\"x\":93},\"playerName\":\"%s\"}"%(self.__player_id,self.__username)
        self.send(4420,msg) 
        #npc
        for i in range(6):
            msg = "["+str(i)+"]"
            self.send(4422,msg)
        id = random.randint(0,7)
        msg = "[" +str(id) +']'
        self.send(4408,msg)


    def kingdom_hegemony(self):
        pass
        #main info
        msg = '[]'
        self.send(4350,msg)
        #self.recv()
        #haixuan tiaozhan
        msg = "["+str(self.__times+1)+"]"
        self.send(4360,msg)
        #self.recv()

    def huangdi_war_join(self):
        msg = "[]"
        self.send(3405,msg)

    def Server_plunder_buzhen(self):
        army_no=0
        msg = "["
        msg += str(army_no) + ","
        msg += "8,[-1,127,-1,227,-1,327,427,-1,527]]"
        self.send(23305 ,msg)
        self.send(23309 ,"[]")

    def Server_plunder_mianzhan(self):
        msg="[]"
        self.send(23308,msg)


    def Server_peakwar_sign(self):
        #buzhen
        army_no=0
        msg = "[" + str(army_no) + ","
        msg += "8,[-1,127,-1,227,-1,327,427,-1,527]]"
        self.send(26305,msg)

        army_no=1
        msg = "[" + str(army_no) + ","
        msg += "8,[-1,21727,-1,-1,-1,-1,-1,-1,-1]]"
        self.send(26305,msg)

        army_no=2
        msg = "[" + str(army_no) + ","
        msg += "8,[-1,11527,-1,-1,-1,-1,-1,-1,-1]]"
        self.send(26305,msg)
        self.send(26308,"[]")
        #self.recv()

    def kingdomwar_join(self): 
        print "kingdomwar_Init"
        self.send(3003,"[]")
        self.send(2403,"[]")
        self.send(1500,"[1,9999]")
        self.send(1502,"[]")
        self.send(1504,"[]")
        self.send(1506,"[]")
        self.send(2601,"[]")
        self.send(2604,"[]")
        self.send(2619,"[]")
        self.send(2621,"[]")
        #self.recv()

        with open("./gm_manlist.txt","r") as f:
            list_read = f.read().split(",")
            list_ = []
            man_id_1 = []
            man_id_2 = []
            man_id_3 = []
            for i in list_read:
                list_.append(int(i))
            list_random=random.sample(list_,18)
            for i in list_random:
                if list_random.index(i) < 6:
                    man_id_1.append(i)
                elif list_random.index(i) >=6 and list_random.index(i) < 12:
                    man_id_2.append(i)
                else:
                    man_id_3.append(i)
            print "kingdomwar_join:==>\narmy_1:%s\narmy_2:%s\narmy_3:%s" %(man_id_1,man_id_2,man_id_3)
        self.send(2621,"[]")
        self.send(2606,"[0," + str(man_id_1) + "]")
        self.send(2606,"[1," + str(man_id_2) + "]")
        self.send(2606,"[2," + str(man_id_3) + "]")
        #self.recv()


    def kingdomwar_move(self):
        #虎符
        self.send(2613,"[0,1]")
        self.send(2613,"[1,1]")
        self.send(2613,"[2,1]")

        #move~
        # city_id=39
        city_id=random.randint(0,17)
        self.send(2628,"[" +str(city_id) +"]")
        self.send(2603,"[0," +str(city_id) +",0,1]")
        # time.sleep(2)
        self.send(2603,"[1," +str(city_id) +",0,1]")
        # time.sleep(2)
        self.send(2603,"[2," +str(city_id) +",0,1]")
        print "move~~~~~~"
        #self.recv()

    def gm_modify_hougong(self):
        woman_id="[9997,1]"
        print "gm_woman(%s) send~"%(woman_id)
        content = "{\"msg\":["
        content += str(woman_id)
        content += "]}"
        msg = urllib.urlencode({"req_type": "1119","content": content,"player_id": self.__player_id})
        url = Client.GM_URL + "/service?"
        req = urllib2.Request(url,msg)
        res_data = urllib2.urlopen(req)
        res = res_data.read().decode('utf-8')
        print res

    def hougong(self):
        self.send(1674,"[]")
        woman_list="[-1,-1,-1,-1,2]"
        self.send(1653,str(woman_list))

    def worldboss_init(self):
        print "worldboss_join"
        self.send(2150,"[]")


        self.send(1319,"[3]")

        #布阵
        with open("./gm_manlist.txt","r") as f:
            list_read = f.read().split(",")
            list_ = []
            man_id_1 = []
            man_id_2 = []
            man_id_3 = []
            for i in list_read:
                list_.append(int(i))
            list_random=random.sample(list_,18)
            for i in list_random:
                if list_random.index(i) < 6:
                    man_id_1.append(i)
                elif list_random.index(i) >=6 and list_random.index(i) < 12:
                    man_id_2.append(i)
                else:
                    man_id_3.append(i)
        self.send(2155,"[0," + str(man_id_1) + "]")
        self.send(2155,"[1," + str(man_id_2) + "]")
        self.send(2155,"[2," + str(man_id_3) + "]")

    def worldboss_attack(self):
        print "%s->worldboss_attack"%(self.__username)
        #清除cd
        self.send(2163,"[0]")
        self.send(2163,"[1]")
        self.send(2163,"[2]")
        #攻击
        self.send(2156,"[0]")
        self.send(2156,"[1]")
        self.send(2156,"[2]")

    def CampWar_join(self):
        self.send(5009,"[]")


#-------------------- base -----------------------
#-------------------- base -----------------------

    def is_json(self,msg):
         try:
            json_object = json.loads(msg)
         except ValueError, e:
            print "-------- Login False -------- "
            return False
         print "-------- Login True -------- "
         return True

    def send(self,type,data):
        msg = "{\"msg\":"
        msg += data
        msg += "}"
        print "send",type,":",msg
        self.__send(type,msg)


    def recv(self):
        msg = self.__recv()
        if (len(self.__left_msg) != 0):
            msg = self.__left_msg + " " + msg
            self.__left_msg = ""
        total_len = len(msg)
        cur_len = 0
        while(cur_len < total_len):
            base = msg[cur_len : cur_len + Client.MSG_BASE_LEN]
            length, self.__protocol, pid, nid = Client.MSG_BASE.unpack(base)
            left_len = total_len - cur_len
            if (left_len >= length):
                cur_msg = msg[cur_len + Client.MSG_BASE_LEN : cur_len + length]
                self.__convert(cur_msg, length - Client.MSG_BASE_LEN)
                cur_len += length
                if(self.protocol() == 501):
                    continue
                #if(self.protocol() >= 14450 and self.protocol() < 14500):
                print "recv", self.__protocol, ":(", length, ")", cur_msg
            else:
                self.__left_msg = msg[cur_len : -1]
                break


    def socket():
        return self.__socket

    def protocol(self):
        return self.__protocol

    def playerID(self):
        return self.__player_id

    def username(self):
        return self.__username;
        self.__login_req(json_data)

    # private
    def __connect(self):
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__socket.connect(Client.SERVER_ADDR)

    def __convert(self,data,length):
        #加密
        Client.CONVERT_LIB.convert_binary(data,length);

    def __package(self,type,data):
        #_len:uint16,_operate:int32,_netid:int32,_pid:int64
        #MSG_BASE_LEN=_len:uint16 + operate:int32 + netid:int32 + _pid:int64
        origin_value = (len(data) + Client.MSG_BASE_LEN,type,self.__net_id,self.__player_id)
        bytes = Client.MSG_BASE.pack(*origin_value)
        self.__convert(data,len(data))
        bytes += data
        return bytes

    def __login_account(self,json_data):
        login_dic = {
            "user_type": 0,
            "open_id": json_data["openid"],
            "token": str(json_data["key"]),
            "timestamp": json_data["timestamp"],
            "channel_key": 0000010000,
            "version": "",
            "imei": "",
            "server_id": Client.SERVER_ID,
            "custom": "",
            "client_ip": ""}
        dic_msg = {"msg": login_dic}
        msg = json.dumps(dic_msg)
        self.__send(Client.LOGIN_REQ,msg)
        msg = self.__recv()
        msg = msg[Client.MSG_BASE_LEN:-1]
        self.__convert(msg,len(msg))
        print msg
        self.is_json(msg)
        json_msg = {}
        json_msg = json.loads(msg)
        print "login_recv:",json_msg
        self.__player_id = json_msg["msg"]["player_id"]
        # print self.__player_id
        print "Login: ",self.__username," PID: ",self.__player_id

    def __login_req(self):
        self.send(1302,"[]")
        #self.recv()
        self.send(1320,"[]")
        #self.recv()


    def __send(self,type,data):
        self.__socket.sendall(self.__package(type,data))

    def __recv(self):
        return self.__socket.recv(64 * 1024)

    def __create_role(self):
        msg = "[\""
        msg += self.__username
        msg += "\","
        msg += "071]"
        self.send(1322,msg)
        #self.recv()


# g_clientList = []
threads = []
clients = []


def __login(times):
    count=input("Enter count of login_players >")
    user_head=raw_input("Enter head of username >")
    count=int(count)
    times_min = (times - 1) * 100
    times_max = times * count 
    for i in range(times_min,times_max):
        user =user_head + str(i)
        # user = "cat"
        # user += str(i)
        # user="lkj9"
        # user = "cat25"
        # password = "aaaaaa"
        c = Client(user,123,i,count)
        # c = Client(user,password,i)
        c.register()
        c.login()
        # c.wanneng()
        if (c.playerID() != 0):
            # c.kingdomwar_join()
            clients.append(c)
        print "------- %s Done --------"%(user)


def __listen(clients):
    while True:
        for player in clients:
            # player.chat_send("熊猫")
            # player.biwu_move()
            # player.talk("cat")
            # player.kingdomwar_move()
            # player.wanneng()
            player.worldboss_attack()
            player.worldboss_init()
            # time.sleep(1)
            player.heartbeat()
            if clients.index(player)==len(clients)-1:
                time.sleep(5)


                # while True:
                #     for player in clients:
                #         player.heartbeat()
                #         if clients.index(player)==len(clients)-1:
                #             time.sleep(5)
                #         else:
                #             pass
            else:
                pass


# *************main
def main():
    t1 = threading.Thread(target=__login(1,))
    # t2 = threading.Thread(target=__listen(clients))q
    # t1.start()
    # t2.start()
    threads.append(t1)
    # threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()


try:
    if __name__ == '__main__':
        main()

# def restart():
# 	os.execl("/usr/bin/python","python","./client.py")

except KeyboardInterrupt:
    print "key break!"
    __login.c.__del__
    pass

except Exception:
    print "debug:"
    traceback.print_exc()

    if not os.path.exists("./Logs"):
        os.mkdir("./Logs")
    logname = time.strftime('%Y_%m_%d_%H%M', time.localtime(time.time()))+'.log'
    log_path = './Logs/'
    logfile = log_path + logname
    #make a logger module
    logging.basicConfig(filename=logfile, filemode="w", level=logging.DEBUG)
    logging.error("wrong info",exc_info=True)

finally:
    print "program Finish!"
    sys.exit()
    # restart()


