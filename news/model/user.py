__author__ = 'kongkongyzt'
from common import *
from hashlib import md5

class User(Base):
    __tablename__='news_user'

    id=Column(Integer,primary_key=True)
    username=Column(String(40))
    password=Column(String(40))
    lastip=Column(String(20))
    lasttime=Column(Integer)


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
            userObj=session.query(User).filter(User.id==id)
            if password:

                changeDict={'password':md5(password).hexdigest()}
            elif lastip and lasttime:
                changeDict={'lastip':lastip,'lasttime':lasttime}
            userObj.update(changeDict)
            session.commit()
            return True








Base.metadata.create_all(engine)



