__author__ = 'kongkongyzt'
from flask import Flask
from news import config
app = Flask(__name__)
app.secret_key = 'fuck'
import news.controller.index

if not config.DEBUG:
    import news.controller.errorHandler
    import news.controller.log
