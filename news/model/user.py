__author__ = 'kongkongyzt'
from common import *
from hashlib import md5

class User(Base):
    __tablename__='news_user'

    id=Column(Integer,primary_key=True)
    username=Column(String(40))
    password=Column(String(40))
    lastip=Column(String(20))
    lasttime=Column(Integer,default=0)


    def updateInfo(self,id=None,username=None,password=None,lastip=None,lasttime=None):
        if id:
            userObj=session.query(User).filter(User.id==id)
            if password:
                changeDict={'password':md5(password).hexdigest()}
            elif lastip and lasttime:
                changeDict={'lastip':lastip,'lasttime':lasttime}
            userObj.update(changeDict)
            session.commit()
            return True
        elif username:
            userObj=session.query(User).filter(User.username==username)
            if password:

                changeDict={'password':md5(password).hexdigest()}
            elif lastip and lasttime:
                changeDict={'lastip':lastip,'lasttime':lasttime}
            userObj.update(changeDict)
            session.commit()
            return True
    def validate(self,username,password):

        user=session.query(User).filter(User.username==username).first()
        if user:
            if user.password==md5(password).hexdigest():
                return True
            else:
                return False
        else:
            return False
    def getUserObj(self,username=None,id=None):
        if username!=None:
            user=session.query(User).filter(User.username==username).first()
            if user:
                return user
            else:
                return False
        elif id!=None:
            user=session.query(User).filter(User.id==id).first()
            if user:
                return user
            else:
                return False

    def addUser(self,username,password):
        userObj=User(username=username,password=md5(password).hexdigest())
        if userObj:
            session.add(userObj)
            session.commit()
            return True
        else:
            return False

    def getAllUsers(self):
        return session.query(User)

    def deleteUser(self,userid):
        userObj=self.getUserObj(id=userid)
        if userObj:
            session.delete(userObj)
            session.commit()
            return True
        else:
            return False

    def getUserList(self):
        users=self.getAllUsers()
        user_list=[]
        for user in users:
            user_list.append(user.username)
        return user_list





Base.metadata.create_all(engine)



