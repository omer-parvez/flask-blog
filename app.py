
"""
    The `import sqlite3` statement is importing the `sqlite3` module, which is a built-in module in
    Python that provides an interface for working with SQLite databases.
"""
import sqlite3 as sq3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    """
    The function `get_db_connection` returns a connection to a SQLite database with row factory
    set to `sqlite3.Row`.
    :return: a SQLite database connection object.
    """
    conn = sq3.connect('database.db')
    conn.row_factory = sq3.Row
    return conn

def get_post(post_id):
    """
    The function `get_post` retrieves a post from a database based on its ID.
    
    :param post_id: The post_id parameter is the unique identifier of the post
    that we want to retrieve from the database
    :return: the post with the specified post_id from the database.
    """
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id=?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = '0X1111X8888'

@app.route("/")
def index():
    """
    The function retrieves all posts from the database and renders them on the index.html template.
    :return: the rendered template "index.html" with the variable "posts" passed as an argument.
    """
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    """
    The function "post" retrieves a post with a given ID and renders it using a template called
    "post.html".
    
    :param post_id: The post_id parameter is the unique identifier for a specific post. It is used
    to retrieve the post from the database or any other data source
    :return: the rendered template 'post.html' with the post data.
    """
    content = get_post(post_id)
    return render_template('post.html', post=content)

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method =='POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        else:
            conn=get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?,?)',
                        (title, content))
            conn.commit()
            conn.close()
            return( redirect(url_for('index')))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']

        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content=?, WHERE id = ?',
                        (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST', ))
def delete(id):
    post=get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id=?', (id, ))
    conn.commit()
    conn.close()
    flash(f"{post['title']} was successfully deleted")
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')



if __name__== "__main__":
    app.run(debug=True)
    