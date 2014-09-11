#encoding=utf8
__author__ = 'kongkongyzt'
import news.config as config
from news import app
from flask import request,render_template,session
import news.model.user as db_user



@app.route('/user/changepwd',methods=['GET','POST'])
def changepwd():
    if request.method == 'GET':
        return render_template('changepwd.html')
    else:
        if not(session['id'] and session['username'] and session['password']):
            
            username=session['username']
            oldpassword=request.form['oldpassword']
            if username!='' and oldpassword!='':
                if db_user.User().validate(username,oldpassword):

                    newpassword=request.form['newpassword']
                    renewpassword=request.form['renewpassword']
                    if newpassword!='':
                        if renewpassword!='':
                            if newpassword==renewpassword:
                                if db_user.User().updateUserInfo(id=session['id'],password=newpassword):
                                    return 'success'
                                else:
                                    return '修改时发生错误'
                            else:
                                return '两次密码不一致'
                        else:
                            return '请确认密码'
                    else:
                        return '请输入新密码'
                else:
                    return '旧密码不正确'
            else:
                return '请输入用户名/密码'





