#encoding:utf8
import time
from news import app
from flask import render_template

@app.template_filter('timeformat')
def timeformat_filter(t,formatstr):
    return time.strftime(formatstr,time.localtime(int(t)))

def pagination(totalElements,currentPage,pageSize,preLink,paginationSize):
    totalPage=(totalElements+pageSize-1)/pageSize
    return render_template('front/pagination.html',totalElements=totalElements,pageSize=pageSize,totalPage=totalPage,preLink=preLink,currentPage=currentPage,paginationSize=5)


@app.template_filter('timeformat')
def timeformat_filter(t,formatstr):
    return time.strftime(formatstr,time.localtime(int(t)))
