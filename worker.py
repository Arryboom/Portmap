# -*- coding: utf-8 -*-
import json
import sqlite3 as sql
import uuid
import os
from subprocess import Popen
import praser
import signal

class errorp:
    def __init__(self):
        self.sucess=False
        self.errorcode=0
    def se(self,x):
        self.sucess=x
    def sc(self,y):
        self.errorcode=y
def newtask(ip,port):
    global conn
    global cursor
    global cudir
    runresult=errorp()
    runresult.se(False)
    try:
        fname=str(uuid.uuid4())+".result"
        runresult.sc(1)
        cursor.execute("select id from tasks where resultfile=?", [fname])
        runresult.sc(2)
        tmpr = cursor.fetchall()
        runresult.sc(3)
        tmprl=len(tmpr)
        while tmprl!=0:
            fname = str(uuid.uuid4()) + ".result"
            cursor.execute("select id from tasks where resultfile=?", [fname])
            tmpr = cursor.fetchall()
            tmprl = len(tmpr)
        runresult.sc(4)
        ports=",".join(port.split("|"))
        runresult.sc(5)
        # openstatus=Popen([cudir+r"/scanner/masscan"," -p"+ports+" "+ip+" -oL "+cudir+"/result/"+fname])
        openstatus = Popen(
            [cudir + r"/scanner/masscan", "-p", ports,ip,"-oL",cudir + "/result/" + fname])
        runresult.sc(6)
        pid=openstatus.pid
        cursor.execute("INSERT INTO TASKS (CIDR,PORT,STATUS,RESULTFILE,PID) VALUES (?,?,?,?,?)",[ip,port,1,fname,pid])
        conn.commit()
        runresult.sc(7)
        conn.commit()
        taskid=cursor.lastrowid
        tmpp={}
        tmpp["taskid"]=taskid
        runresult.sc(8)
        runresult.se(True)
    except Exception,e:
        # print Exception,e
        return json.dumps(runresult.__dict__)
    runresult.sc(0)
    return json.dumps(dict(runresult.__dict__,**tmpp))
    #-p80,8000-8100 10.0.0.0/8
def stoptask(taskid):
    global conn
    global cursor
    global cudir
    er=errorp()
    er.se(False)
    try:
        cursor.execute("select pid from tasks where id=?",[taskid])
        er.sc(1)
        tmpr=cursor.fetchall()
        er.sc(2)
        if len(tmpr)==0:
            er.sc(3)
            pass
        pid=tmpr[0][0]
        er.sc(4)
        try:
            os.kill(pid,signal.SIGKILL)
        except Exception:
            pass
        er.sc(5)
        cursor.execute("update tasks set status=? where id=?",[2,taskid])
        er.sc(6)
    except Exception:
        return json.dumps(er.__dict__)
    er.se(True)
    er.sc(0)
    return json.dumps(er.__dict__)


def restarttask(taskid):
    global conn
    global cursor
    global cudir
    ###################
    er=errorp()
    er.se(False)
    er.sc(1)
    stoptask(taskid)
    try:
        cursor.execute("select CIDR,PORT,RESULTFILE from tasks where id=?",[taskid])
        er.sc(2)
        tmpr=cursor.fetchall()
        if len(tmpr)!=0:
            er.sc(3)
            CIDR=tmpr[0][0]
            port=tmpr[0][1]
            fname=tmpr[0][2]
            er.sc(4)
            openstatus = Popen([cudir + r"/scanner/masscan",
                               " -p" + port + " " + CIDR + " -oL " + cudir + "/result/" + fname])
            er.sc(5)
            pid=openstatus.pid
            cursor.execute("update tasks set pid=?,status=?",[pid,1])
            er.sc(6)
            conn.commit()
            er.sc(7)
        else:
            er.se(False)
            er.sc(400)
            return json.dumps(er.__dict__)
    except Exception:
        return json.dumps(er.__dict__)
    er.se(True)
    er.sc(0)
    return json.dumps(er.__dict__)
def getresult(taskid):
    global conn
    global cursor
    global cudir

    er=errorp()
    try:
        er.sc(1)
        cursor.execute("select RESULTFILE from tasks where id=?",[taskid])
        er.sc(2)
        tmpr=cursor.fetchall()
        er.sc(3)
        if len(tmpr)!=0:
            fname=tmpr[0][0]
            print fname
            er.sc(4)
            suc,result=praser.parse(fname)
            er.sc(5)
            if suc:
                tr={}
                tr["result"]=result
                er.sc(6)
                er.se(True)
                er.sc(0)
                return json.dumps(dict(er.__dict__,**tr))
            else:
                return json.dumps(er.__dict__)
        else:
            er.sc(400)
            return json.dumps(er.__dict__)
    except Exception:
        return json.dumps(er.__dict__)

def taskdetail(taskid):
    global conn
    global cursor
    global cudir
    try:
        er=errorp()
        er.se(False)
        er.sc(1)
        cursor.execute("select CIDR,PORT,ADD_TIME,STATUS from tasks where id=?",[taskid])
        er.sc(2)
        tmpr=cursor.fetchone()
        er.sc(3)
        if len(tmpr)!=0:
            CIDR=tmpr[0]
            PORT=tmpr[1]
            ADD_TIME=tmpr[2]
            STATUS=tmpr[3]
            er.sc(4)
            sresult={}
            sresult["IP"]=CIDR
            sresult["PORTS"]=PORT
            sresult["ADD_TIME"]=ADD_TIME
            sresult["STATUS"]=STATUS
            er.sc(5)
        else:
            er.sc(400)
            return json.dumps(er.__dict__)
    except Exception:
        return json.dumps(er.__dict__)
    er.se(True)
    er.sc(0)
    return json.dumps(dict(er.__dict__,**sresult))
def deltask(taskid):
    global conn
    global cursor
    global cudir
    pass
    er=errorp()
    try:
        er.sc(1)
        cursor.execute("select resultfile,pid from tasks where id=?",[taskid])
        er.sc(2)
        tmpr=cursor.fetchone()
        er.sc(3)
        if len(tmpr)!=0:
            fname=tmpr[0]
            pid=tmpr[1]
            er.sc(4)
            try:
                os.kill(pid,signal.SIGKILL)
            except Exception:
                pass
            er.sc(5)
            os.remove(cudir+r"/result/"+fname)
            er.sc(6)
            cursor.execute("delete from tasks where id=?",[taskid])
            conn.commit()
            er.sc(7)
        else:
            er.sc(400)
            return json.dumps(er.__dict__)
    except Exception:
        return json.dumps(er.__dict__)
    er.se(True)
    er.sc(0)
    return json.dumps(er.__dict__)
def cleartasks():
    global conn
    global cursor
    global cudir

    er=errorp()
    try:
        er.sc(1)
        cursor.execute("select pid,resultfile from tasks;")
        er.sc(2)
        tmpr=cursor.fetchall()
        er.sc(3)
        if len(tmpr)!=0:
            er.sc(4)
            for everytmpr in tmpr:
                er.sc(5)
                pid=everytmpr[0]
                fname=everytmpr[1]
                try:
                    os.kill(pid)
                    os.remove(fname)
                except:
                    pass
            er.sc(6)
            cursor.execute("delete from tasks;")
            cursor.execute("delete from sqlite_sequence where name='tasks'; ")
            er.sc(7)
            conn.commit()
            er.sc(8)
        else:
            er.sc(400)
            return json.dumps(er.__dict__)
    except Exception:
        return json.dumps(er.__dict__)
    er.se(True)
    er.sc(0)
    return json.dumps(er.__dict__)
def tasklist():
    global conn
    global cursor
    global cudir
    er=errorp()
    try:
        er.sc(1)
        cursor.execute("select id from tasks")
        er.sc(2)
        tmpr=cursor.fetchall()
        er.sc(3)
        if len(tmpr)!=0:
            ids=[]
            er.sc(4)
            for everyr in tmpr:
                id=everyr[0]
                ids.append(id)
                er.sc(5)
        else:
            er.sc(400)
            return json.dumps(er.__dict__)
    except Exception:
        return json.dumps(er.__dict__)
    er.se(True)
    er.sc(0)
    ids_d={}
    ids_d["idlist"]=ids
    return json.dumps(dict(er.__dict__,**ids_d))


if __name__=="worker":
    global conn
    global cursor
    global cudir
    cudir=os.getcwd()
    conn=sql.connect("scan.db3")
    cursor=conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")
    if len(cursor.fetchall())==0:
        cursor.execute(
            "CREATE TABLE tasks (ID INTEGER PRIMARY KEY AUTOINCREMENT,CIDR TEXT NOT NULL,PORT TEXT,STATUS INT,RESULTFILE text,PID INT,ADD_TIME datetime DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()
    ##==========###=======###=======###=======###=======###=======###=======###=======###=======###=======###=======###=======###
    Popen(["python",cudir+"/checker.py"])
    #TEST
    # newtask("1999.55.5","80|99|77|774537")
    # e=errorp()
    # print e
    # e.se(True)
    # e.sc(3)
    # print e.__dict__
    # print json.dumps(e.__dict__)








# C:\junk\so>type \junk\so\scriptpath\script1.py
# import sys, os
# print "script: sys.argv[0] is", repr(sys.argv[0])
# print "script: __file__ is", repr(__file__)
# print "script: cwd is", repr(os.getcwd())
# import whereutils
# whereutils.show_where()
#
# C:\junk\so>type \python26\lib\site-packages\whereutils.py
# import sys, os
# def show_where():
#     print "show_where: sys.argv[0] is", repr(sys.argv[0])
#     print "show_where: __file__ is", repr(__file__)
#     print "show_where: cwd is", repr(os.getcwd())
#
# C:\junk\so>\python26\python scriptpath\script1.py
# script: sys.argv[0] is 'scriptpath\\script1.py'
# script: __file__ is 'scriptpath\\script1.py'
# script: cwd is 'C:\\junk\\so'
# show_where: sys.argv[0] is 'scriptpath\\script1.py'
# show_where: __file__ is 'C:\\python26\\lib\\site-packages\\whereutils.pyc'
# show_where: cwd is 'C:\\junk\\so'