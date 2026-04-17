from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


class BlogPost:
    """Class to manage blog posts"""
    def __init__(self, posts, id=None):
        self._posts = posts
        self._id_list = []
        for post in posts:
            self._id_list.append(post['id'])
        if id == None:
            self._id = len(self.posts) + 1
        else:
            self._id = id

    @property
    def posts(self):
        """returns list of posts"""
        return self._posts

    def add(self, author, title, content):
        """Adds a post"""
        self._posts.append({"id": self._id, 'author': author, 'title': title, 'content': content})
        self._id_list.append(self._id)
        self._id += 1

    def delete(self, id):
        """Delets a post"""
        post_index = self._id_list.index(id)
        del self._id_list[post_index]
        del self._posts[post_index]


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


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    blog_posts.delete(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        pass
    # Update the post in the JSON file
    # Redirect back to index

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
