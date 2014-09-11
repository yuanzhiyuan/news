from news import app
from news.model.article import Article

@app.route('/article/<int:id>')
def viewArticle(id):
    Article().getArticle(id)
    return 'request finished'