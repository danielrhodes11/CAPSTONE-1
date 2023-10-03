import os
from unittest import TestCase
from models import db, User, Playlists, PlaylistTracks
from config.test_config import *
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from app import app

bcrypt = Bcrypt()
os.environ["FLASK_ENV"] = "testing"


class BaseTestCase(TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test."""
        db.session.rollback()
        with app.app_context():
            db.drop_all()


class TestPlaylistModel(BaseTestCase):
    def test_playlist_model(self):
        """Test playlist model."""
        user = User.register(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            profile_image="static/test-img.png",
            bio="Test bio"
        )
        db.session.add(user)
        db.session.commit()

        playlist = Playlists(
            title="Test Playlist",
            description="Test description",
            image="static/test-img.png",
            user_id=user.id
        )
        db.session.add(playlist)
        db.session.commit()

        self.assertEqual(playlist.title, "Test Playlist")
        self.assertEqual(playlist.description, "Test description")
        self.assertEqual(playlist.image, "static/test-img.png")
        self.assertEqual(playlist.user_id, user.id)

    def test_playlist_model_fail(self):
        """Test playlist model failure."""
        user = User.register(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            profile_image="static/test-img.png",
            bio="Test bio"
        )
        db.session.add(user)
        db.session.commit()

        playlist = Playlists(
            title="Test Playlist",
            description="Test description",
            image="static/test-img.png",
            user_id=user.id
        )
        db.session.add(playlist)
        db.session.commit()

        user2 = User.register(
            username="testuser2",
            password="testpassword2",
            email="test2@example.com",
            first_name="Test2",
            last_name="User2",
            profile_image="static/test-img2.png",
            bio="Test bio2"
        )

        playlist2 = Playlists(
            title="Test Playlist",
            description="Test description",
            image="static/test-img.png",
            user_id=user2.id
        )

        db.session.add(playlist2)

        with self.assertRaises(IntegrityError):
            db.session.commit()


class TestPlaylistTracksModel(BaseTestCase):
    def test_playlist_tracks_model(self):
        """Test playlist tracks model."""
        user = User.register(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            profile_image="static/test-img.png",
            bio="Test bio"
        )
        db.session.add(user)
        db.session.commit()

        playlist = Playlists(
            title="Test Playlist",
            description="Test description",
            image="static/test-img.png",
            user_id=user.id
        )

        db.session.add(playlist)
        db.session.commit()

        playlist_track = PlaylistTracks(
            playlist_id=playlist.id,
            title="Test Track",
            artist="Test Artist",
            album="Test Album",
            image="static/test-img.png",
            release_date="2020-01-01",
            spotify_id="6rqhFgbbKwnb9MLmUQDhG6"
        )

        db.session.add(playlist_track)
        db.session.commit()

        self.assertEqual(playlist_track.playlist_id, playlist.id)

    def test_playlist_tracks_model_fail(self):
        """Test playlist tracks model failure."""
        user = User.register(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            profile_image="static/test-img.png",
            bio="Test bio"
        )

        db.session.add(user)
        db.session.commit()

        playlist = Playlists(
            title="Test Playlist",
            description="Test description",
            image="static/test-img.png",
            user_id=user.id
        )

        db.session.add(playlist)
        db.session.commit()

        playlist_track = PlaylistTracks(
            playlist_id=playlist.id,
            title="Test Track",
            artist="Test Artist",
            album="Test Album",
            image="static/test-img.png",
            release_date="2020-01-01",
            spotify_id="6rqhFgbbKwnb9MLmUQDhG6"
        )

        db.session.add(playlist_track)
        db.session.commit()

        playlist_track2 = PlaylistTracks(
            playlist_id=playlist.id,
            title="Test Track",
            artist="Test Artist",
            album="Test Album",
            image="static/test-img.png",
            release_date="2020-01-01",
            spotify_id="6rqhFgbbKwnb9MLmUQDhG6"
        )

        db.session.add(playlist_track2)

        with self.assertRaises(IntegrityError):
            db.session.commit()
