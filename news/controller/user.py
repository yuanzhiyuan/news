#encoding=utf8
__author__ = 'kongkongyzt'
import news.config as config
from news import app
from flask import request,render_template



@app.route('/user/changepwd',methods=['GET','POST'])
def changepwd():
    if request.method == 'GET':
        return render_template('changepwd.html')
    else:
        pass




