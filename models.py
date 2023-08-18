"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_img = "https://cdn-icons-png.flaticon.com/512/552/552721.png"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = default_img)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    db.app = app
    db.init_app(app)

