from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)


class BlogPost:
    """Manage blog posts in JSON."""

    def __init__(self, filename):
        self.filename = filename
        self._posts = self._load_data()

    def _load_data(self):
        """Reads data from file or returns empty"""
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self):
        """Saves data into in JSON."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self._posts, f, indent=4)

    @property
    def posts(self):
        """Returns list of blog posts."""
        return self._posts

    def add(self, author, title, content):
        """Adds and saves blog post. Sets id to max(id)+1"""
        new_id = max([p['id'] for p in self._posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "like": 0
        }
        self._posts.append(new_post)
        self._save_data()

    def delete(self, post_id):
        """Deletes post with selected number."""
        self._posts = [p for p in self._posts if p['id'] != post_id]
        self._save_data()

    def fetch_post_by_id(self, post_id):
        """Fetches blog post with selected id."""
        for post in self._posts:
            if post['id'] == post_id:
                return post
        return None

    def fetch_post_position_by_id(self, post_id):
        """Fetches blog post position with selected id."""
        i = 0
        for post in self._posts:
            if post['id'] == post_id:
                return i
            i += 1
        return None

    def change(self, post_id, author, title, content):
        """Changes blog post with selected id.
        Resets likes to 0."""
        changed_post = {
            "id": post_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0,
        }
        post_index = self.fetch_post_position_by_id(post_id)
        self._posts[post_index] = changed_post
        self._save_data()

    def like(self, post_id):
        """Updates like by one"""
        post_index = self.fetch_post_position_by_id(post_id)
        self._posts[post_index]["like"] += 1
        self._save_data()


blog_posts = BlogPost("posts.json")


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
    post = blog_posts.fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts.change(post_id, author, title, content)
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    blog_posts.like(post_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
