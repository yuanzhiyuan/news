__author__ = 'kongkongyzt'
from common import *

class Article(Base):
    __tablename__='news_article'

    id=Column(Integer,primary_key=True)
    categoryid=Column(Integer)
    title=Column(String(70))
    publisher=Column(String(20))
    author=Column(String(20))
    editor=Column(String(20))
    publishTime=Column(Integer,default=0)
    updateTime=Column(Integer,default=0)
    content=Column(Text)
    views=Column(Integer,default=0)
    state=Column(Integer,default=0)
    checker1=Column(String(20))
    checker2=Column(String(20))


    def getArticle(self,id):
        test=session.query(Article).filter(Article.id == id).first()
        print test,'========='
        return test