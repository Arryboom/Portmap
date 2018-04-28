#Install
下载编译https://github.com/robertdavidgraham/masscan
```
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
cp /bin/masscan /portmap/scanner/
python run.py
```

##所有接口均使用POST传参和调用,默认端口为8080，可以在run.py进行修改

**newtask**
- ip
- ports

>新建任务，IP可以是CIDR格式，如127.0.0.0/24或192.168.1.8,ports使用|分割，如80|3389|8080|9000
请求ex:
```ip=192.168.0.0/24&ports=22|80|3389```
响应ex:
{"errorcode": 0, "sucess": true, "taskid": 4}

**stoptask**
- taskid

>停止任务，taskid为新建任务时或从tasklist中获取的任务ID
请求ex:
```taskid=3```
响应ex:
{"errorcode": 0, "sucess": true}

**restarttask**
- taskid

>重新启动任务，taskid为新建任务时或从tasklist中获取的任务ID
请求ex:
```taskid=3```
响应ex:
{"errorcode": 0, "sucess": true}

**getresult**
- taskid

>获取扫描结果，taskid为新建任务时或从tasklist中获取的任务ID
请求ex:
```taskid=3```
响应ex:
{"errorcode": 0, "sucess": true, "result": {"192.168.0.17": {"timestamp": "1524884727", "port": "3389"}, "192.168.0.30": {"timestamp": "1524884723", "port": "80"}, "192.168.0.37": {"timestamp": "1524884723", "port": "3389"}, "192.168.0.36": {"timestamp": "1524884724", "port": "3389"}, "192.168.0.34": {"timestamp": "1524884724", "port": "3389"}, "192.168.0.39": {"timestamp": "1524884727", "port": "3389"}, "192.168.0.19": {"timestamp": "1524884725", "port": "3389"}, "192.168.0.16": {"timestamp": "1524884725", "port": "3389"}, "192.168.0.99": {"timestamp": "1524884727", "port": "80"}, "192.168.0.98": {"timestamp": "1524884726", "port": "80"}, "192.168.0.95": {"timestamp": "1524884726", "port": "80"}, "192.168.0.108": {"timestamp": "1524884725", "port": "3389"}, "192.168.0.92": {"timestamp": "1524884725", "port": "80"}, "192.168.0.93": {"timestamp": "1524884726", "port": "3389"}, "192.168.0.41": {"timestamp": "1524884728", "port": "3389"}, "192.168.0.64": {"timestamp": "1524884723", "port": "3389"}, "192.168.0.66": {"timestamp": "1524884724", "port": "3389"}, "192.168.0.61": {"timestamp": "1524884726", "port": "3389"}, "192.168.0.49": {"timestamp": "1524884722", "port": "3389"}, "192.168.0.21": {"timestamp": "1524884727", "port": "80"}, "192.168.0.23": {"timestamp": "1524884722", "port": "80"}, "192.168.0.25": {"timestamp": "1524884728", "port": "3389"}, "192.168.0.27": {"timestamp": "1524884726", "port": "80"}, "192.168.0.254": {"timestamp": "1524884727", "port": "80"}, "192.168.0.81": {"timestamp": "1524884724", "port": "80"}, "192.168.0.84": {"timestamp": "1524884727", "port": "80"}, "192.168.0.6": {"timestamp": "1524884725", "port": "80"}, "192.168.0.51": {"timestamp": "1524884726", "port": "3389"}, "192.168.0.50": {"timestamp": "1524884727", "port": "3389"}, "192.168.0.53": {"timestamp": "1524884726", "port": "3389"}, "192.168.0.55": {"timestamp": "1524884723", "port": "3389"}, "192.168.0.54": {"timestamp": "1524884723", "port": "3389"}, "192.168.0.79": {"timestamp": "1524884727", "port": "3389"}, "192.168.0.59": {"timestamp": "1524884728", "port": "3389"}, "192.168.0.70": {"timestamp": "1524884726", "port": "3389"}}}

**taskdetail**
- taskid

>获取任务详情，taskid为新建任务时或从tasklist中获取的任务ID
请求ex:
```taskid=3```
响应ex:
{"errorcode": 0, "STATUS": 1, "IP": "192.168.0.0/24", "sucess": true, "PORTS": "80|3389", "ADD_TIME": "2018-04-28 03:05:22"}
参数说明：
STATUS是任务状态，
1.扫描中
2.停止
3.完成
4.空结果（为扫描到任何开放端口和存活主机）
0.异常退出

**deltask**
- taskid

>删除任务，taskid为新建任务时或从tasklist中获取的任务ID
请求ex:
```taskid=3```
响应ex:
{"errorcode": 0, "sucess": true}

**cleartasks**
- None

>清空任务池，无需任何参数
响应ex:
{"errorcode": 0, "sucess": true}

**tasklist**
- None

>获取任务列表，无需任何参数
响应ex:
{"errorcode": 0, "sucess": true, "idlist": [1, 2, 3]}



#响应说明
返回值均为JSON格式，success为bool值表明请求是否处理成功，errorcode为错误码，在success为false时调试使用。