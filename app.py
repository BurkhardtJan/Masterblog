from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

class BlogPost:
    def __init__(self, posts, id = None):
        self._posts = posts
        if id == None:
            self._id = len(self.posts) + 1
        else:
            self._id = id

    @property
    def posts(self):
        return self._posts

    def add(self, author, title, content):
        self._posts.append({id: self._id, 'author': author, 'title': title, 'content': content})
        self._id += 1

init_blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
]
blog_posts = BlogPost(init_blog_posts)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts.posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts.add(author, title, content)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
