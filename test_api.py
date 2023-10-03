import os
from unittest import TestCase
from unittest.mock import patch
from models import db, User
from config.test_config import *
from app import app, CURR_USER_KEY
from api import get_token  # Import the get_token function

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

    # Mock the get_token function
    def test_get_token(self, mock_get_token):
        # Call the function under test
        token = get_token()

        # Assertions
        self.assertIsNotNone(token)
        self.assertEqual(token, 'mocked_token')
