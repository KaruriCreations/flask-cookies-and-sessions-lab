#!/usr/bin/env python3

# Python 3.14 Compatibility Monkeypatches:
# Older versions of pytest (7.2.0) and werkzeug (2.2.2) rely on deprecated/removed ast module attributes
# (like ast.Str, ast.NameConstant, and the .s / .n properties on Constant).
# These patches dynamically restore them for runtime compatibility on Python 3.14.
import ast
if not hasattr(ast, 'Str'):
    ast.Str = ast.Constant
if not hasattr(ast, 'NameConstant'):
    ast.NameConstant = ast.Constant
if not hasattr(ast.Constant, 's'):
    ast.Constant.s = property(lambda self: self.value, lambda self, val: setattr(self, 'value', val))
if not hasattr(ast.Constant, 'n'):
    ast.Constant.n = property(lambda self: self.value, lambda self, val: setattr(self, 'value', val))


from flask import Flask, make_response, jsonify, session

from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0
    session['page_views'] += 1

    if session['page_views'] > 3:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)

    article = Article.query.filter_by(id=id).first()
    if not article:
        return make_response(jsonify({'message': 'Article not found'}), 404)

    return make_response(jsonify(ArticleSchema().dump(article)), 200)



if __name__ == '__main__':
    app.run(port=5555)
