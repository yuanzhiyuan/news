__author__ = 'yuan,kongkongyzt'
from common import *

class Category(Base):
    __tablename__='news_category'

    id=Column(Integer,primary_key=True)
    parentid=Column(Integer)
    categoryname=Column(String(40))

    def getAllCategory(self):
        return session.query(Category)

    def getChildId(self,parentid):
        return session.query(Category).filter(Category.parentid == parentid).all()

    def getCategoryObj(self,id=None,name=None):
        if id:
            return session.query(Category).filter(Category.id == id).first()
        elif name:
            return session.query(Category).filter(Category.categoryname == name).first()
        else:
            return False

    def getCategoryByLevel(self,level):
        if level==1:
            return session.query(Category).filter(Category.parentid == 0).all()
        elif level==2:
            return session.query(Category).filter(Category.parentid != 0).all()
        else:
            return False

    def addCategory(self,parentid,categoryname):
        categoryObj=Category(parentid=parentid,categoryname=categoryname)
        if categoryObj:
            session.add(categoryObj)
            session.commit()
            return True
        else:
            return False

    def deleteCategory(self,id):
        category=session.query(Category).filter(Category.id==id).first()
        if not category:
            return False
        session.delete(category)
        session.commit()
        return True

    def getCategoryDict(self,categories):

        category_dict={}
        for category in categories:
            category_dict[category.id]=category.categoryname
        return category_dict

    def getChildCategory(self,id):
        return session.query(Category).filter(Category.parentid == id).all()

    def getCategortByid(self,id):
        return session.query(Category).filter(Category.id == id).first()
        
    def getTopCategoryid(self,id):
        parentid=id
        while parentid !=0:
            parentid=session.query(Category).filter(Category.id == parentid).first().parentid
            if parentid==0:
                return id
            else:
                id=parentid

    def renameCategory(self,categoryid,categoryname):
        category=session.query(Category).filter(Category.id==categoryid)
        if not category:
            return False
        category.update({"categoryname":categoryname})
        session.commit()
        return True
