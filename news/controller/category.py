from news import app
from news.model.article import Article
from flask import abort

@app.route('/category/<int:id>')
def viewCategory(id):
    if id:
        pass
    else:
        raise abort(404)