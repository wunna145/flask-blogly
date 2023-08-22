"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import inspect
from models import db, connect_db, User, Post, Tag

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

    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("/posts/new.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new/add", methods=["POST"])
def new_post(user_id):
    new = Post(
        title = request.form['title'],
        content = request.form['content'],
        user_id=user_id
    )
    tag_ids = [int(id) for id in request.form.getlist("tags")]
    new.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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
    tags = Tag.query.all()
    return render_template("/posts/edit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_form(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'],
    post.content = request.form['content'],
    post.user_id = post.user_id

    tag_ids = [int(id) for id in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return render_template("/posts/detail.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def tag():
    tags = Tag.query.all()
    return render_template("/tags/index.html", tags=tags)

@app.route("/tags/new")
def new_tag_form():
    posts = Post.query.all()
    return render_template("/tags/new.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def new_tag():
    post_ids = [int(id) for id in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new = Tag(name=request.form['name'], posts=posts)

    db.session.add(new)
    db.session.commit()
    flash(f"Tag '{new.name}' added.")
    return redirect('/tags')

@app.route("/tags/<int:tag_id>")
def tags_show(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def tag_edit_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit.html', tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(id) for id in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Taf '{tag.name}' edited")
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")