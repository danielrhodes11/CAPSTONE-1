"""schema for databse for spotify clon using spotify api"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

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
    profile_image = db.Column(
        db.Text, nullable=False, default="https://www.pngitem.com/pimgs/m/30-307416_profile-icon-png-image-free-download-searchpng-employee.png")

    playlists = db.relationship(
        "Playlist", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, email, first_name, last_name, profile_image):
        """register user w/hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name, profile_image=profile_image)

    @classmethod
    def authenticate(cls, username, password):
        """validate that user exists and password is correct"""

        user = User.query.filter_by(username=username).first()

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


class Playlists(db.Model):
    """playlists table"""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="cascade"), nullable=False)

    songs = db.relationship(
        "Song", secondary="playlist_songs", backref="playlists")

    def serialize(self):
        """serialize playlist data"""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "user_id": self.user_id
        }


class PlaylistSongs(db.Model):
    """playlist songs table"""

    __tablename__ = "playlist_songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey(
        "playlists.id", ondelete="cascade"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey(
        "songs.id", ondelete="cascade"), nullable=False)

    def serialize(self):
        """serialize playlist songs data"""

        return {
            "id": self.id,
            "playlist_id": self.playlist_id,
            "song_id": self.song_id
        }


class Song(db.Model):
    """songs table"""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)
    album = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text, nullable=False)
    preview = db.Column(db.Text, nullable=False)
    spotify_id = db.Column(db.Text, nullable=False)

    def serialize(self):
        """serialize song data"""

        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "image": self.image,
            "genre": self.genre,
            "release_date": self.release_date,
            "preview": self.preview,
            "spotify_id": self.spotify_id
        }
