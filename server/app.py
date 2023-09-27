#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

#set an intial count to the play
@app.before_request
def before_request():
    session.setdefault('page_views', 0)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Query all articles from the database
    articles = Article.query.all()

    # Create a list to store article data
    article_list = []

    # Iterate through the articles and convert them to dictionaries
    for article in articles:
        article_data = {
            'id': article.id,
            'author': article.author,
            'title': article.title,
            'content': article.content,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date.strftime('%Y-%m-%d %H:%M:%S')  # Convert date to string
        }
        article_list.append(article_data)

    # Return the list of articles as JSON
    return jsonify(article_list), 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Check if the user has viewed more than 3 pages
    if session['page_views'] >= 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Increment the page_views counter
    session['page_views'] += 1

    # Fetch the article data from your Article model by ID
    article = Article.query.get(id)

    # Check if the article exists
    if article is None:
        return jsonify({'message': 'Article not found'}), 404

    # Create a response object
    response = make_response(jsonify({
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date.strftime('%Y-%m-%d %H:%M:%S')  # Convert date to string
    }))

    # You can set additional headers if needed
     # Set the Content-Type header to indicate JSON response
    response.headers['Content-Type'] = 'application/json'

    return response, 200

if __name__ == '__main__':
    app.run(port=5555)
