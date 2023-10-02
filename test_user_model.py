import os
from unittest import TestCase
from models import db, User  # Import db from models module
from config.test_config import *
from app import app, CURR_USER_KEY
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt  # Import Bcrypt


bcrypt = Bcrypt()

os.environ["FLASK_ENV"] = "testing"


class UserModelTestCase(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        """Set up the test environment."""
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        # Create the database tables in the test environment
        with app.app_context():
            db.create_all()

        # Create a test client
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test."""
        # Rollback any database transactions
        db.session.rollback()

        # Drop all tables to reset the database
        with app.app_context():
            db.drop_all()

    def test_user_register(self):
        """Test user registration."""
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

        registered_user = User.query.get(user.id)
        self.assertIsNotNone(registered_user)
        self.assertEqual(registered_user.username, "testuser")
        self.assertEqual(registered_user.email, "test@example.com")

    def test_user_register_fail(self):
        """Test user registration failure."""
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

        user2 = User.register(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            profile_image="static/test-img.png",
            bio="Test bio"
        )
        db.session.add(user2)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_authenticate(self):
        """Test user authentication."""
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

        authenticated_user = User.authenticate("testuser", "testpassword")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")
        self.assertEqual(authenticated_user.email, "test@example.com")

    def test_user_authenticate_fail(self):
        """Test user authentication failure."""
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

        authenticated_user = User.authenticate("testuser", "wrongpassword")
        self.assertFalse(authenticated_user)

    def test_user_serialize(self):
        """Test user serialization."""
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

        serialized_user = user.serialize()
        self.assertEqual(serialized_user["username"], "testuser")
        self.assertEqual(serialized_user["email"], "test@example.com")
        self.assertEqual(serialized_user["first_name"], "Test")
        self.assertEqual(serialized_user["last_name"], "User")
        self.assertEqual(serialized_user["profile_image"],
                         "static/test-img.png")

    def test_user_repr(self):
        """Test user representation."""
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

        self.assertEqual(repr(user), "<User testuser test@example.com>")
