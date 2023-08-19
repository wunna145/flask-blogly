"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import inspect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'applesarenotbananas'

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    inspector = inspect(db.engine)
    if not (inspector.has_table('users') and inspector.has_table('posts')):
        db.create_all()

@app.route("/")
def root():
    return redirect("/users")

@app.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    return render_template('/users/user_list.html', users = users)

@app.route("/users/new", methods=["GET"])
def new():
    return render_template('/users/new.html')

@app.route("/users/new", methods=["POST"])
def add():
    new = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/users/detail.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("/posts/new.html", user=user)

@app.route("/users/<int:user_id>/posts/new/add", methods=["POST"])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    new = Post(
        title = request.form['title'],
        content = request.form['content'],
        user_id=user_id
    )

    db.session.add(new)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("/posts/detail.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("/posts/edit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_form(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'],
    post.content = request.form['content'],
    post.user_id = post.user_id

    db.session.add(post)
    db.session.commit()

    return render_template("/posts/detail.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

