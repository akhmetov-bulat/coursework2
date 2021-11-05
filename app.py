import json
from flask import Flask, request, Response, render_template

app = Flask(__name__)


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_json = f.read()
        if not raw_json:
            return []
        return json.loads(raw_json)


@app.route('/')
def index():
    data = read_json('data/data.json')
    comments = read_json('data/comments.json')
    bookmarks = read_json('data/bookmarks.json')
    return render_template('index.html',bookmarks = bookmarks, data = data, comments = comments)



if __name__ == '__main__':
    app.run(debug=True)
