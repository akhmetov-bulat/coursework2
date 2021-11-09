from utils import read_json, write_json, get_all_posts,get_posts_by_keyword, get_bookmarks
from flask import Flask, request, Response, render_template, redirect

app = Flask(__name__)


@app.route('/')
def index():
    posts, bookmarks_count = get_all_posts()
    return Response(render_template('index.html', posts=posts, bookmarks_count=bookmarks_count), status=200)


@app.route('/posts/<int:postid>')
def post(postid:int):
    posts, bookmarks_count = get_posts_by_keyword('pk', postid)
    print(posts)
    return Response(render_template('post.html', post=posts[0]), status=200)


@app.route('/search/', methods=['GET'])
def search_get():
    search_request = request.args.get("s")
    search = True if search_request else False
    if search_request:
        posts, bookmarks_count = get_posts_by_keyword('content', search_request)
        return Response(render_template('search.html', posts=posts), search = search)
    return Response(render_template('search.html'), status = 400)


@app.route('/users/<username>')
def user_posts(username):
    posts, bookmarks_count = get_posts_by_keyword('poster_name', username)
    return Response(render_template('user-feed.html', posts=posts, bookmarks_count=bookmarks_count),status=200)


@app.route('/tag/<tagname>')
def tag_posts(tagname):
    posts, bookmarks_count = get_posts_by_keyword('content', '#' + tagname)
    return Response(render_template('tag.html', posts=posts), status=200)


@app.route('/bookmarks')
def bookmarks_posts():
    posts = get_bookmarks()
    return Response(render_template('bookmarks.html', posts=posts), status=200)


@app.route('/bookmarks/add/<int:postid>')
def add_bookmark(postid:int):
    bookmarks = read_json('data/bookmarks.json')
    if postid not in bookmarks:
        bookmarks.append(postid)
    write_json('data/bookmarks.json', bookmarks)
    return redirect(request.environ.get('HTTP_REFERER', request.remote_addr), code=302)


@app.route('/bookmarks/remove/<int:postid>')
def remove_bookmark(postid:int):
    bookmarks = read_json('data/bookmarks.json')
    if postid in bookmarks:
        bookmarks.remove(postid)
    write_json('data/bookmarks.json', bookmarks)
    return redirect(request.environ.get('HTTP_REFERER', request.remote_addr), code=302)


if __name__ == '__main__':
    app.run(debug=True)
