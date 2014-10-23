#encoding:utf8
__author__ = 'yuan'
from functools import wraps
from flask import url_for,redirect,session,request


def requires_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' in session:
            #@DEBUG print '/'.join(request.url.split('/')[3:])
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))



    return wrapped





