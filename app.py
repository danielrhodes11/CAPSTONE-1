import os
from flask import Flask, render_template, redirect, flash, session, request, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Playlist, Song, PlaylistSong
from forms import RegisterForm, LoginForm, PlaylistForm, SongForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from config.dev_config import DevConfig
from config.test_config import TestConfig

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config.from_object(DevConfig)
# Determine the Flask environment and load the appropriate configuration


if os.environ.get('FLASK_ENV') == 'testing':
    app.config.from_object(TestConfig)
elif os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevConfig)

toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
#


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If there already is a user with that username: flash message
    and re-present form.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                profile_image=form.profile_image.data
            )
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)
