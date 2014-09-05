__author__ = 'yuan'
from common import *

class User(Base):
    __tablename__='news_user'

    id=Column(Integer,primary_key=True)
    username=Column(String(20))
    password=Column(String(40))
