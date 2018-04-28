# -*- coding: utf-8 -*-
import os

def parse(fname):
    global cudir
    fpath=cudir+r"/result/"+fname
    size=os.path.getsize(fpath)
    result={}
    if size!=0:
        with open(fpath) as rfile:
            for line in rfile:
                if line.find("open")>=0:
                    everyparamsinline=line.split()
                    ip, port, timestamp = everyparamsinline[3], everyparamsinline[2], everyparamsinline[4]
                    tmpr = {}
                    # tmpr["ip"] = ip
                    tmpr["port"] = port
                    tmpr["timestamp"] = timestamp
                    if ip in result.keys():
                        tmpx=result[ip]
                        tmpx["port"]=tmpx["port"]+"|"+tmpr["port"]
                        tmpx["timestamp"]=tmpr["timestamp"]
                        result[ip]=tmpx
                    else:
                        result[ip]=tmpr
    else:
        return False,result
    #need do some check here
    return True,result
if __name__=="praser":
    global cudir
    cudir=os.getcwd()
