from utils import read_json, write_json
from flask import Flask, request, Response, render_template, redirect

app = Flask(__name__)


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
    comments = []
    bookmarks = read_json('data/bookmarks.json')
    marked = False
    for index in range(len(data)):
        if data[index]['pk'] == postid:
            data[index]["views_count"] = data[index]["views_count"] + 1
            post = data[index]
            break
    write_json('data/data.json', data)
    for comment in all_comments:
        if postid == comment["post_id"]:
            comments.append(comment)
    if postid in bookmarks:
        marked = True
    return render_template('post.html', post=post, comments=comments, marked=marked)


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


@app.route('/tag/<tagname>')
def tag_posts(tagname):
    tagname = "#" + tagname
    tags_posts = []
    comments = read_json('data/comments.json')
    bookmarks = read_json('data/bookmarks.json')
    data = read_json('data/data.json')
    for post in data:
        if tagname in post['content']:
            tags_posts.append(post)
    return render_template('tag.html', tags_posts=tags_posts, comments=comments, bookmarks=bookmarks)


@app.route('/bookmarks')
def bookmarks_posts():
    bookmarked_posts = []
    comments = read_json('data/comments.json')
    bookmarks = read_json('data/bookmarks.json')
    data = read_json('data/data.json')
    for post in data:
        if post['pk'] in bookmarks:
            bookmarked_posts.append(post)
    return render_template('bookmarks.html', bookmarked_posts=bookmarked_posts, comments=comments, bookmarks=bookmarks)


@app.route('/bookmarks/add/<int:postid>')
def add_bookmark(postid:int):
    bookmarks = read_json('data/bookmarks.json')
    if postid not in bookmarks:
        bookmarks.append(postid)
    write_json('data/bookmarks.json', bookmarks)
    # print(request.environ.get('HTTP_REFERER', request.remote_addr))
    return redirect(request.environ.get('HTTP_REFERER', request.remote_addr), code=302)


@app.route('/bookmarks/remove/<int:postid>')
def remove_bookmark(postid:int):
    bookmarks = read_json('data/bookmarks.json')
    if postid in bookmarks:
        bookmarks.remove(postid)
    write_json('data/bookmarks.json', bookmarks)
    # print(request.environ.get('HTTP_REFERER', request.remote_addr))
    return redirect(request.environ.get('HTTP_REFERER', request.remote_addr), code=302)


if __name__ == '__main__':
    app.run(debug=True)
