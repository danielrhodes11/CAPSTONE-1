"""schema for databse for spotify clon using spotify api"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Relationship
from sqlalchemy import String


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    """users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_image = db.Column(
        db.Text, nullable=False, default="static/default-img.png")

    playlists = db.relationship(
        "Playlists", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, email, first_name, last_name, profile_image, bio):
        """register user w/hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name, profile_image=profile_image, bio=bio)

    @classmethod
    def authenticate(cls, username, password):
        """validate that user exists and password is correct"""

        user = User.query.filter_by(username=username).first()
        # if warning add session

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def serialize(self):
        """serialize user data"""

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profile_image": self.profile_image
        }

    def __repr__(self):
        """show info about user"""

        return f"<User {self.username} {self.email}>"


class Playlists(db.Model):
    """playlists table"""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="cascade"), nullable=False)

    tracks = db.relationship(
        "PlaylistTracks", backref="playlist", cascade="all, delete-orphan")

    def serialize(self):
        """serialize playlist data"""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "user_id": self.user_id
        }


class PlaylistTracks(db.Model):
    """playlist tracks table"""

    __tablename__ = "playlist_tracks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey(
        "playlists.id", ondelete="cascade"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)
    album = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text, nullable=False)
    preview = db.Column(db.Text, nullable=True)
    spotify_id = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint(
        'playlist_id', 'spotify_id', name='unique_playlist_track'),)

    def serialize(self):
        """serialize playlist tracks data"""

        return {
            "id": self.id,
            "playlist_id": self.playlist_id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "image": self.image,
            "genre": self.genre,
            "release_date": self.release_date,
            "preview": self.preview,
            "spotify_id": self.spotify_id,
        }


# learn about ordinality     https://stackoverflow.com/questions/5033547/sqlalchemy-order-by-descending

# collection class for playlist tracks


# create a class that handles request calls to spotify api in a seperate file
