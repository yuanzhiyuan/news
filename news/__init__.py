__author__ = 'kongkongyzt'
from flask import *
from news import config
app = Flask(__name__)
app.secret_key = 'fuck'
import news.controller.index
import news.controller.user
import news.controller.article
import news.controller.category

if not config.DEBUG:
    import news.controller.errorHandler
    import news.controller.log
