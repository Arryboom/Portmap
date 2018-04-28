# -*- coding: utf-8 -*-

import sqlite3 as sql
from time import sleep
import psutil
import os

def eternalchecker():
    global conn
    global cursor
    global curdir
    while True:
        pids=psutil.pids()
        cursor.execute("select id,pid,resultfile from tasks where status=?",[1])
        tmpr=cursor.fetchall()
        if tmpr:
            if len(tmpr)!=0:
                for everytmpr in tmpr:
                    id=everytmpr[0]
                    pid=everytmpr[1]
                    resultfile=everytmpr[2]
                    if pid in pids:
                        continue
                    else:
                        if os.path.exists(cudir+"/result/"+resultfile):
                            fsize=os.path.getsize(cudir+"/result/"+resultfile)
                            if fsize>0:
                                cursor.execute("update tasks set status=? where id=?",[3,id])
                                conn.commit()
                            else:
                                cursor.execute("update tasks set status=? where id =?",[4,id])
                                conn.commit()
                        else:
                            cursor.execute("update tasks set status=? where id =?", [0, id])
                            conn.commit()
            else:
                sleep(10)
                continue
        else:
            sleep(10)
            continue
        sleep(5)

if __name__!="checker":
    global conn
    global cursor
    global cudir
    cudir=os.getcwd()
    conn=sql.connect("scan.db3")
    cursor=conn.cursor()
    eternalchecker()









 # 1 #!/usr/bin/python
 #
 #  2
 #
 #  3 import psutil
 #
 #  4
 #
 #  5 pids = psutil.pids()
 #
 #  6 for pid in pids:
 #
 #  7     p = psutil.Process(pid)
 #
 #  8     print("pid-%d,pname-%s" %(pid,p.name()))



# import psutil
#
# for proc in psutil.process_iter():
#     try:
#         pinfo = proc.as_dict(attrs=['pid', 'name'])
#     except psutil.NoSuchProcess:
#         pass
#     else:
#         print(pinfo)