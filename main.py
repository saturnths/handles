#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask.json import jsonify
from search import Search

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/api/search', methods=["GET", "POST"])
def api():
    if request.method == 'POST':
        json = request.json
        searcher = Search(json['urls'])
        results = searcher.get_handles(json['mode'])

        return jsonify(results)

if __name__ == "__main__":
    app.run()
