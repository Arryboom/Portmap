# -*- coding: utf-8 -*-
from bottle import route, run,request,post
import worker


@route('/index')
def index():
    return "Wscanner Console"
#====================================================================================================================
@post('/newtask')
def r_newtask():
    cidr=request.forms.get('ip')
    port=request.forms.get('ports')
    return worker.newtask(cidr,port)
#====================================================================================================================
@post('/stoptask')
def r_stop():
    id=request.forms.get('taskid')
    return worker.stoptask(id)
#====================================================================================================================
@post('/restarttask')
def r_restart():
    id = request.forms.get('taskid')
    return worker.restarttask(id)
#====================================================================================================================
@post('/getresult')
def r_getresult():
    id = request.forms.get('taskid')
    return worker.getresult(id)
#====================================================================================================================
@post('/taskdetail')
def r_taskdetail():
    id = request.forms.get('taskid')
    return worker.taskdetail(id)
#====================================================================================================================
@post('/deltask')
def r_deltask():
    id = request.forms.get('taskid')
    return worker.deltask(id)
#====================================================================================================================
@post('/cleartasks')
def r_cleartasks():
    return worker.cleartasks()
@post('/tasklist')
def r_tasklist():
    return worker.tasklist()

#--------------------------------------------------------------------------------------------------------------------
run(host='0.0.0.0', port=8080)









# from bottle import get, post, request # or route
#
# @get('/login') # or @route('/login')
# def login():
#     return '''
#         <form action="/login" method="post">
#             Username: <input name="username" type="text" />
#             Password: <input name="password" type="password" />
#             <input value="Login" type="submit" />
#         </form>
#     '''
#
# @post('/login') # or @route('/login', method='POST')
# def do_login():
#     username = request.forms.get('username')
#     password = request.forms.get('password')
#     if check_login(username, password):
#         return "<p>Your login information was correct.</p>"
#     else:
#         return "<p>Login failed.</p>"
