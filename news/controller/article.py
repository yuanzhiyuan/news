# -*- coding: utf-8 -*-
__author__ = 'yuan'
import sys
from news import app
from news.controller.auth import requires_auth
import news.model.category as db_category
import news.model.user as db_user
import news.model.article as db_article
from news.controller.tools import pagination
from flask import render_template,request,abort,session
reload(sys)
sys.setdefaultencoding('utf8')

# @app.route('/article/list/<limitKey>/<limitValue>/page/<int:pageNum>')
# @app.route('/article/list/<limitKey>/<limitValue>/')
@app.route('/article/list/')
@app.route('/article/list/page/<int:pageNum>')

@requires_auth
def listArticle(pageNum=1):
    limitDict={'all':None,'categoryid':0,'editor':1,'state':2}
    limitKey='all'
    limitValue='all'
    if limitValue=='all':
        limitValue=None


    # 获取所有指标信息
    category_dict=db_category.Category().getCategoryDict(db_category.Category().getAllCategory())
    # editor_list=db_user.User().getUserList()

    # 获取所有文章
    allArticles=db_article.Article().getAllArticles()

    # 获取目标文章
    targetArticles=db_article.Article().getArticleByAOrderByB(article=allArticles,A=limitDict[limitKey],A_value=limitValue,B=0)


    # departmentUser=db_user.User().getUserByAOrderByB(user=db_user.User().getAllUsers(),A=1,A_value=departmentid)

    # allUsers=db_user.User().getUserByAOrderByB(user=departmentUser,role=3,A=limitDict[limitKey],A_value=limitValue,B=0)
    # testers=db_user.User().getUserByAOrderByB(user=departmentUser,role=2)
    # if targetArticles.count()==0:
    #     return render_template('manage/article/listArticle_none.html',category_dict=category_dict,editor_list=editor_list)
    # return str(allUsers)

    total,pages,articles=db_article.Article().cutArticles(targetArticles,pageNum)
    # return 'hehe'
    # if pages<=9:
    #       enum = range(pages)
    # else:
    #       if pageNum<5:
    #           enum = range(9)
    #       elif pageNum+5>pages:
    #           enum = range(pages)[-9:]
    #       else:@app.route('article/list/')

    #           enum = range(pages)[pageNum-4:pageNum+5]

    # testers=db_user.User().getUserByAOrderByB(user=departmentUser,role=2)
    paginationHTML=pagination(total,currentPage=pageNum,pageSize=20,preLink='/article/list/page/',paginationSize=5)
    return render_template('manage/article/admin-manageArticle.html',category_dict=category_dict,paginationHTML=paginationHTML,articles=articles,totalPages=pages,currentPage=pageNum)

@app.route('/article/view/<int:articleid>')
@requires_auth
def viewArticle(articleid):
    articleObj=db_article.Article().getArticle(id=articleid)
    if articleObj:
        articleObj.views+=1
        return render_template('manage/article/viewArticle.html',article=articleObj)
    else:
        return abort(404)


@app.route('/article/delete',methods=['POST'])
@requires_auth
def deleteArticle():
    articleid=request.form['articleid']

    if db_article.Article().deleteArticle(id=int(articleid)):
        return 'success'
    else:
        return 'failed'

@app.route('/article/<int:id>')

def viewfrontArticle(id):
    article=db_article.Article().getArticleByid(id)
    if article:
        article.updateViews(id)
        category=db_category.Category().getCategortByid(article.categoryid)
        topid=db_category.Category().getTopCategoryid(category.id)
        return render_template('front/article.html',article=article,category=category,title=article.title+"|未来网新闻",topid=topid)
    else:
        return abort(404)

@app.route('/article/verify/<int:state>',methods=['POST'])
@requires_auth
def verifyArticle(state):
    # return 'zzzz'
    articleid=request.form['articleid']
    # return 'aaa'
    if db_article.Article().verifyArticle(id=int(articleid),state=state,username=session['username']):
        return 'success'
    else:
        return 'failed'

@app.route('/article/action/<string:action>',methods=['GET','POST'])
@app.route('/article/action/<string:action>/<int:articleid>',methods=['GET','POST'])

@requires_auth
def addArticle(action,articleid=1):
    if request.method=='GET':
        topCategory=db_category.Category().getCategoryByLevel(level=1)
        category_dict=db_category.Category().getCategoryDict(categories=topCategory)
        if action=='add':
            return render_template('manage/article/admin-addArticle.html',category_dict=category_dict,mode=0)
        elif action=='update':
            article=db_article.Article().getArticle(id=articleid)
            title=article.title
            content=article.content
            publisher=article.publisher
            author=article.author
            return render_template('manage/article/admin-addArticle.html',articleid=articleid,category_dict=category_dict,mode=1,title=title,content=content,publisher=publisher,author=author)



    categoryid=request.form['categoryid']
    title=request.form['title']
    content=request.form['content']
    publisher=request.form['publisher']
    author=request.form['author']
    editor=session['username']
    if categoryid=='':
        return '请选择板块'
    if title=='':
        return '请输入标题'
    if content=='':
        return '请输入内容'
    if action=='add':
        db_article.Article().addArticle(categoryid=categoryid,title=title,publisher=publisher,author=author,editor=editor,content=content)

        return 'success'
    elif action=='update':
        db_article.Article().updateArticle(articleid=articleid,categoryid=categoryid,title=title,publisher=publisher,author=author,content=content)

        return 'success'
