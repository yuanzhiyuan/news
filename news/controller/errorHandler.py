#encoding:utf8
from news import app
from flask import request

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('ERROR:500'+':'+' IP:'+request.remote_addr+' REQUEST URL:'+request.base_url)
    app.logger.error('Header:'+str(request.headers))
    return "<center><h1>Oop~~</h1><p>服务器发生了故障，我们正在紧急修复中，请耐心等待</p></center>"

@app.errorhandler(403)
def forbidden_error(error):
    app.logger.info('ERROR:403'+':'+' IP:'+request.remote_addr+' REQUEST URL:'+request.base_url)
    app.logger.info('Header:'+str(request.headers))
    return '<center><h1>抱歉，您无权访问此页面</h1></center>'

@app.errorhandler(404)
def notFound_error(error):
    app.logger.info('ERROR:404'+':'+' IP:'+request.remote_addr+' REQUEST URL:'+request.base_url)
    app.logger.info('Header:'+str(request.headers))
    return "<center><h1 style='font-size:108px'>:(</h1><p>抱歉，您请求的网页不存在</p></center>"
