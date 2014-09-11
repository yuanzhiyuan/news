__author__ = 'kongkongyzt'
from common import *

class Category(Base):
    __tablename__='news_category'

    id=Column(Integer,primary_key=True)
    parentid=Column(Integer)
    name=Column(String(40))