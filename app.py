from flask import Flask, request, render_template, redirect, url_for
from blog_post_handler import BlogPost

app = Flask(__name__)

blog_posts = BlogPost("posts.json")


@app.route('/')
def index():
    """Index page"""
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts.posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """GET: Formular to add a new blog post.
    POST: Add a new blog post"""
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts.add(author, title, content)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by ID"""
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    blog_posts.delete(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Updates a blog post by ID"""
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
    """Like a blog post by ID"""
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    blog_posts.like(post_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
