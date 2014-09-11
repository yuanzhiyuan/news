__author__ = 'kongkongyzt'
import news.config as config
from news import app

@app.route('/')
def index():
    return 'hello world'

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form['username']
        password=request.form['password']
        if username:
            if password:
                if db_user.User().validate(username=username,password=password):
                    userObj=db_user.User().getUserObj(username=username)
                    session['id']=userObj.id
                    session['username']=username
                    session['password']=password
                    return 'success'
                else:
                    return 'error1'
            else:
                return 'error2'
        else:
            return 'error3'
