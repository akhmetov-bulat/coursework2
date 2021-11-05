import json
from flask import Flask, request, Response, render_template

app = Flask(__name__)


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_json = f.read()
        if not raw_json:
            return []
        return json.loads(raw_json)


def write_json(filename,json_data):
    with open(filename, 'w', encoding='utf-8',) as f:
        json.dump(json_data, f, ensure_ascii=False, indent='\t')

@app.route('/')
def index():
    data = read_json('data/data.json')
    comments = read_json('data/comments.json')
    bookmarks = read_json('data/bookmarks.json')
    return render_template('index.html',bookmarks = bookmarks, data = data, comments = comments)


@app.route('/posts/<int:postid>')
def post(postid:int):
    data = read_json('data/data.json')
    all_comments = read_json('data/comments.json')
    cur_comments = []
    bookmarks = read_json('data/bookmarks.json')
    marked = False
    for index in range(len(data)):
        if data[index]['pk'] == postid:
            data[index]["views_count"] = data[index]["views_count"] + 1
            cur_post = data[index]
            break
    write_json('data/data.json', data)
    for comment in all_comments:
        if postid == comment["post_id"]:
            cur_comments.append(comment)
    if postid in bookmarks:
        marked = True
    return render_template('post.html', post=cur_post, comments=cur_comments, marked=marked)


@app.route('/search/', methods=['GET'])
def search_get():
    search_request = request.args.get("s")
    found_posts = []
    search = False
    comments = read_json('data/comments.json')
    bookmarks = read_json('data/bookmarks.json')
    if search_request:
        search = True
        data = read_json('data/data.json')
        for post in data:
            if search_request.casefold() in post['content'].casefold():
                found_posts.append(post)
    return render_template('search.html', found_posts=found_posts[0:10],
                           search=search, comments=comments, bookmarks=bookmarks)


@app.route('/users/<username>')
def user_posts(username):
    users_posts = []
    comments = read_json('data/comments.json')
    bookmarks = read_json('data/bookmarks.json')
    data = read_json('data/data.json')
    for post in data:
        if post['poster_name'] == username:
            users_posts.append(post)
    return render_template('user-feed.html', users_posts=users_posts, comments=comments, bookmarks=bookmarks)



if __name__ == '__main__':
    app.run(debug=True)
