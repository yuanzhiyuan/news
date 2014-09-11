import news.config as config
from news import app

@app.route('/article/<int:id>')
def viewArticle(id):
    pass