__author__ = 'yuan'
from common import *

class Article(Base):
    __tablename__='news_article'

    id=Column(Integer,primary_key=True)
    title=Column(String(70))
    publisher=Column(String(20))
    author=Column(String(20))
    editor=Column(String(20))
    publishTime=Column(Integer,default=0)
    content=Column(Text)
    views=Column(Integer,default=0)
    state=Column(Integer,default=0)