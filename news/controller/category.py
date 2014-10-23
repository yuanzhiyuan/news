# -*- coding: utf-8 -*-
import sys
from news import app
from flask import abort,request,render_template,session,redirect,jsonify
import news.model.category as db_category
import news.model.article as db_article
from news.controller.auth import requires_auth
from news.controller.tools import pagination
reload(sys)
sys.setdefaultencoding('utf8')

@app.route('/category/<int:id>')
@app.route('/category/<int:id>/page/<int:currentpage>')
def viewCategory(id,currentpage=1):
    category=db_category.Category().getCategortByid(id)
    topid=db_category.Category().getTopCategoryid(id)
    if category:
        childCategory=db_category.Category().getChildCategory(id)
        if childCategory:
            tmpArray=[]
            for singleCategory in childCategory:
                total,articleList=db_article.Article().getArticleByCategoryid(singleCategory.id,order='reverse')
                tmpDict=dict(articleList=articleList,categoryid=singleCategory.id,categoryname=singleCategory.categoryname)
                tmpArray.append(tmpDict)
            return render_template('front/multiple-list.html',listBlock=tmpArray,category=category,topid=topid,title=category.categoryname+"板块二级目录")
        else:
            total,articleList=db_article.Article().getArticleByCategoryid(id,page=currentpage,order='reverse')
            paginationHTML=pagination(total,currentPage=currentpage,pageSize=16,preLink='/category/'+str(id)+'/page/',paginationSize=5)
            return render_template('front/list.html',articleList=articleList,paginationHTML=paginationHTML,category=category,topid=topid,title=category.categoryname+"板块")
    else:
        return abort(404)

# @app.route('/category/add',methods=['POST'])
@app.route('/category/add/',methods=['POST','GET'])
@requires_auth
def addCategory():
    if request.method=='GET':

            parents=db_category.Category().getCategoryByLevel(level=1)
            return render_template('manage/category/addCategory.html',parents=parents)

    else:
        parentid=request.form['parentid']
        # return 'ssfas'

        categoryname=request.form['categoryname']

        if categoryname=='':
            return '请输入板块名'
        if db_category.Category().getCategoryObj(name=categoryname):
            return '板块名已存在'
        db_category.Category().addCategory(parentid=parentid,categoryname=categoryname)
        return 'success'


@app.route('/category/list')
@requires_auth
def listCategory():

    allCategory=db_category.Category().getAllCategory()
    categoryid_count_dict={}
    categoryid_name_dict={}
    categoryid_name_dict[0]="无"
    for category in allCategory:
        categoryid=category.id
	categoryname=category.categoryname
        count=db_article.Article().getCountOfCategory(categoryid=categoryid)
        categoryid_count_dict[categoryid]=count
	categoryid_name_dict[categoryid]=categoryname

    return render_template('manage/category/listCategory.html',allCategory=allCategory,categoryid_count_dict=categoryid_count_dict,categoryid_name_dict=categoryid_name_dict)


@app.route('/category/delete',methods=['POST'])
@requires_auth
def deleteCategory():

    categoryid=request.form['categoryid']
    if db_category.Category().deleteCategory(id=int(categoryid)):
        return 'success'
    else:
        return 'failed'

@app.route('/category/getchildid',methods=['POST'])
@requires_auth
def getchildid():
    parentid=request.form['categoryid']
    child=db_category.Category().getChildId(parentid=parentid)
    child_id_name_dict=db_category.Category().getCategoryDict(child)
    return jsonify({'childcategory':child_id_name_dict})


@app.route('/category/rename',methods=['POST'])
@requires_auth
def renameCategory():
    categoryid=request.form['categoryid']
    categoryname=request.form['categoryname']
    if categoryname=='':
        return '板块名称不能为空'
    if db_category.Category().renameCategory(categoryid=categoryid,categoryname=categoryname):
        return 'success'
    return '参数错误'
