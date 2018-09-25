from flask import Flask, jsonify, request
from .reader import FeedReader

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to RSS Feeds Reader'})

@app.route('/rss_feed/read')
def read():
    url = request.args.get('url')

    if not url:
        return jsonify({'message': 'Please enter rss url.'}), 403

    reader = FeedReader(url)

    return jsonify({'message': '', 'data': reader.feeds})
