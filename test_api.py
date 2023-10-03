import os
from unittest import TestCase
from unittest.mock import patch
from models import db, User
from config.test_config import *
from app import app, CURR_USER_KEY
from api import get_token, get_genres, get_songs_by_genre, is_valid_spotify_id

os.environ["FLASK_ENV"] = "testing"


class TestSpotifyApi(TestCase):
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

    def test_get_token(self):
        """Test get_token function."""
        token = get_token()
        self.assertIsInstance(token, str)

    def test_get_genres(self):
        """Test get_genres function."""
        token = get_token()
        genres = get_genres(token)
        self.assertIsInstance(genres, list)

    def test_get_songs_by_genre(self):
        """Test get_songs_by_genre function."""
        token = get_token()
        tracks = get_songs_by_genre(token, "country")
        self.assertIsInstance(tracks, list)

    def test_is_valid_spotify_id(self):
        """Test is_valid_spotify_id function."""
        token = get_token()
        valid_id = "6rqhFgbbKwnb9MLmUQDhG6"
        invalid_id = "invalid_id"
        self.assertTrue(is_valid_spotify_id(token, valid_id))
        self.assertFalse(is_valid_spotify_id(token, invalid_id))
