#encoding=utf8
__author__ = 'kongkongyzt'
import news.config as config
from news import app
from flask import request,render_template,session,redirect
import news.model.user as db_user
from news.controller.auth import requires_auth
@app.route('/admin')
@requires_auth
def admin():
    return render_template('manage/shouldknow.html')

@app.route('/shouldknow')
@requires_auth
def shouldKnow():
    return render_template('manage/shouldknow.html')



@app.route('/user/changepwd',methods=['GET','POST'])
@requires_auth
def changepwd():
    if request.method == 'GET':
        return render_template('manage/user/changepwd.html')
    else:


            
        username=session['username']
        oldpassword=request.form['oldpassword']
        if not(username!='' and oldpassword!=''):
            return '请输入用户名/密码'
        if not db_user.User().validate(username,oldpassword):
            return '旧密码不正确'

        newpassword=request.form['newpassword']
        renewpassword=request.form['renewpassword']
        if not newpassword!='':
            return '请输入新密码'
        if not renewpassword!='':
           return '请确认密码'
        if not newpassword==renewpassword:
            return '两次密码不一致'
        if db_user.User().updateInfo(id=session['id'],password=newpassword):
            return 'success'
        else:
            return '修改时发生错误'


@app.route('/user/add',methods=['GET','POST'])
@requires_auth
def addUser():
    if request.method=='GET':
        return render_template('manage/user/addUser.html')
    else:



        username=request.form['username']
        password=request.form['password']
        repassword=request.form['repassword']
        if username=='':
            return '请输入用户名'
        if password=='':
            return '请输入密码'
        if repassword=='':
            return '请确认密码'
        if password!=repassword:
            return '两次密码不一致'
        if db_user.User().getUserObj(username=username):
            return '用户名已存在'
        db_user.User().addUser(username=username,password=password)
        return 'success'


@app.route('/user/list')
@requires_auth
def listUser():

    allUsers=db_user.User().getAllUsers()
    return render_template('manage/user/listUser.html',allUsers=allUsers)

@app.route('/user/delete',methods=['POST'])
@requires_auth
def deleteUser():

    userid=request.form['userid']
    if db_user.User().deleteUser(userid=int(userid)):
        if int(userid)==session['id']:
            return 'self'
        return 'success'
    else:
        return 'failed'









