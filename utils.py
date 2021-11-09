import json


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_json = f.read()
        if not raw_json:
            return []
        return json.loads(raw_json)


def write_json(filename,json_data):
    with open(filename, 'w', encoding='utf-8',) as f:
        json.dump(json_data, f, ensure_ascii=False, indent='\t')


def increase_view_count(data, post, postid):
    for index in range(len(data)):
        if data[index]['pk'] == postid:
            data[index]["views_count"] = data[index]["views_count"] + 1
            cur_post = data[index]
            break
    write_json('data/data.json', data)


def get_all_posts():
    data = read_json('data/data.json')
    bookmarks = read_json('data/bookmarks.json')
    comments = read_json('data/comments.json')
    posts = []
    for post in data:
        post['marked'] = post['pk'] in bookmarks
        post['comments_count'] = 0
        for comment in comments:
            if comment['post_id'] == post['pk']:
                post['comments_count'] += 1
        post['hashtags'] = []
        text_split = post['content'].split(" ")
        for i in range(len(text_split) - 1,0,-1):
            if text_split[i].startswith('#'):
                post['hashtags'].append(text_split.pop(i))
        post['content'] = ' '.join(text_split)
        posts.append(post)
    return posts, len(bookmarks)


def get_posts_by_keyword(keyword, value):
    data = read_json('data/data.json')
    bookmarks = read_json('data/bookmarks.json')
    comments = read_json('data/comments.json')
    posts = []
    for i in range(len(data), 0, -1):
        if str(value).casefold() in str(data[i-1][keyword]).casefold():
            if keyword == 'pk':
                data[i-1]["views_count"] += 1
            data[i-1]['marked'] = data[i-1]['pk'] in bookmarks
            data[i-1]['comments_count'] = 0
            for comment in comments:
                if comment['post_id'] == data[i-1]['pk']:
                    data[i-1]['comments_count'] += 1
            data[i-1]['hashtags'] = []
            text_split = data[i-1]['content'].split(" ")
            for j in range(len(text_split),0,-1):
                if text_split[j-1].startswith('#'):
                    data[i-1]['hashtags'].append(text_split.pop(j-1))
            data[i-1]['content'] = ' '.join(text_split)
            posts.append(data[i-1])
    return posts, len(bookmarks)


def get_bookmarks():
    data = read_json('data/data.json')
    bookmarks = read_json('data/bookmarks.json')
    comments = read_json('data/comments.json')
    posts = []
    for post in data:
        if post['pk'] in bookmarks:
            post['marked'] = post['pk'] in bookmarks
            post['comments_count'] = 0
            for comment in comments:
                if comment['post_id'] == post['pk']:
                    post['comments_count'] += 1
            post['hashtags'] = []
            text_split = post['content'].split(" ")
            for i in range(len(text_split),0,-1):
                if text_split[i - 1].startswith('#'):
                    post['hashtags'].append(text_split.pop(i))
            post['content'] = ' '.join(text_split)
            posts.append(post)
    return posts
