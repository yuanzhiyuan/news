__author__ = 'kongkongyzt'
import news.config as config
from news import app

@app.route('/')
def index():
    return 'hello world'
