#encoding=utf8
__author__ = 'kongkongyzt'
import time
import news.config as config
from news import app
from flask import request,render_template,session,redirect
import news.model.user as db_user
from news.controller.auth import requires_auth
@app.route('/')
def index():
    session.pop('id',None)
    session.pop('username',None)
    session.pop('role',None)
    return redirect('http://www.future.org.cn')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('/manage/login.html')
    else:
        username=request.form['username']
        password=request.form['password']
        if not username:
            return 'error3'
        if not password:
            return 'error2'
        if not db_user.User().validate(username=username,password=password):
            return 'error1'

        userObj=db_user.User().getUserObj(username=username)
        if not userObj:
            return 'error4'

        session['id']=userObj.id
        session['username']=username
        session['password']=password
        lasttime=int(time.time())
        lastip=request.remote_addr
        # return lastip+lasttime
        db_user.User().updateInfo(username=username,lasttime=lasttime,lastip=lastip)
        return 'success'

@app.route('/logout')
@requires_auth
def logout():
    session.pop('id',None)
    session.pop('username',None)
    session.pop('role',None)
    return redirect('/login')
