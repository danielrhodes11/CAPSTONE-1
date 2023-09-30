import os
from flask import Flask, render_template, redirect, flash, session, g, request, url_for
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Playlists, PlaylistTracks
from forms import RegisterForm, LoginForm, EditUserForm, PlaylistForm, SongForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from config.dev_config import DevConfig
from config.test_config import TestConfig
from api import token, search_for_song, get_song_info

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


@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("home.html")


# USER ROUTES


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
                bio=form.bio.data,
                profile_image=form.profile_image.data
            )
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username/Email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect(f"/users/{user.id}")

    else:
        return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/users/{user.id}")
        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Successfully logged out.", "success")
    return redirect("/login")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user profile"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    playlists = Playlists.query.filter_by(user_id=user_id).all()

    return render_template("user_profile.html", user=user, playlists=playlists)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """Show edit user form and handle edit of user profile"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    if user != g.user:
        raise Unauthorized()

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.profile_image = form.profile_image.data

        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(f"/users/{user_id}")

    return render_template("edit_user.html", form=form, user=user)


@app.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):
    """Delete user"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    if user != g.user:
        raise Unauthorized()

    do_logout()

    db.session.delete(user)
    db.session.commit()

    flash("User deleted!", "success")
    return redirect("/signup")


###################################
#  PLAYLIST ROUTES
###################################

@app.route("/users/<int:user_id>/playlists/new", methods=["GET", "POST"])
def create_playlist(user_id):
    """Show create playlist form and handle creation of playlist"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    if user != g.user:
        raise Unauthorized()

    form = PlaylistForm()

    if form.validate_on_submit():
        playlist = Playlists(
            title=form.title.data,
            description=form.description.data,
            image=form.image.data,
            user_id=user_id
        )

        db.session.add(playlist)
        db.session.commit()

        flash("Playlist created!", "success")
        return redirect(f"/users/{user_id}")

    return render_template("create_playlist.html", form=form, user=user)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show playlist details"""

    playlist = Playlists.query.get_or_404(playlist_id)
    user = User.query.get_or_404(playlist.user_id)

    # Retrieve the playlist tracks associated with the playlist
    playlist_tracks = PlaylistTracks.query.filter_by(
        playlist_id=playlist_id).all()

    return render_template("playlist_details.html", playlist=playlist, user=user, playlist_tracks=playlist_tracks)


@app.route("/playlists/<int:playlist_id>/edit", methods=["GET", "POST"])
def edit_playlist(playlist_id):
    """Show edit playlist form and handle edit of playlist"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    playlist = Playlists.query.get_or_404(playlist_id)

    if playlist.user_id != g.user.id:
        raise Unauthorized()

    form = PlaylistForm(obj=playlist)

    if form.validate_on_submit():
        playlist.title = form.title.data
        playlist.description = form.description.data
        playlist.image = form.image.data

        db.session.commit()
        flash("Playlist updated!", "success")
        return redirect(f"/playlists/{playlist_id}")

    return render_template("edit_playlist.html", form=form, playlist=playlist)


@app.route("/playlists/<int:playlist_id>/delete", methods=["GET", "POST"])
def delete_playlist(playlist_id):
    """Delete playlist"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    playlist = Playlists.query.get_or_404(playlist_id)

    if playlist.user_id != g.user.id:
        raise Unauthorized()

    db.session.delete(playlist)
    db.session.commit()

    flash("Playlist deleted!", "success")
    return redirect(f"/users/{g.user.id}")

########### SEARCH AND ADD SONGS TO PLAYLISTS############


@app.route("/playlists/<int:playlist_id>/search")
def search_for_songs(playlist_id):
    """Show search for songs form"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    playlist = Playlists.query.get_or_404(playlist_id)

    if playlist.user_id != g.user.id:
        raise Unauthorized()

    form = SongForm()

    return render_template("search_for_songs.html", form=form, playlist=playlist)


@app.route("/playlists/<int:playlist_id>/search/results")
def show_search_results(playlist_id):
    """Show search results"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    playlist = Playlists.query.get_or_404(playlist_id)

    if playlist.user_id != g.user.id:
        raise Unauthorized()

    # Get the search term (song_name) from the request arguments
    song_name = request.args.get("song_name")

    if not song_name:
        # Handle the case where there's no song_name provided
        flash("Please enter a song name for the search.", "warning")
        return redirect(f"/playlists/{playlist_id}/search")

    spotify_id = request.args.get("spotify_id")

    # Make a request to the Spotify API to search for songs
    response = search_for_song(token, song_name)

    return render_template("search_results.html", playlist=playlist, songs=response, spotify_id=spotify_id)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["POST"])
def add_song_to_playlist(playlist_id):
    # Get the spotify_id from the form or request data
    spotify_id = request.form.get("spotify_id")

    # Retrieve more information about the song from the Spotify API
    song_info = get_song_info(token, spotify_id)  # Pass the token

    if song_info is not None:
        # Create the PlaylistTracks object with the retrieved information
        playlist_track = PlaylistTracks(
            playlist_id=playlist_id,
            title=song_info["title"],
            artist=song_info["artist"],
            album=song_info["album"],
            image=song_info["image"],
            release_date=song_info["release_date"],
            preview=song_info.get("preview"),
            spotify_id=spotify_id
        )

        db.session.add(playlist_track)
        db.session.commit()

        flash("Song added to playlist successfully!", "success")
    else:
        flash("Failed to add the song to the playlist.", "danger")

    # Redirect back to the playlist details page or wherever you want
    return redirect(url_for("show_playlist", playlist_id=playlist_id))


@app.route("/playlists/<int:playlist_id>/delete-song/<int:playlist_track_id>", methods=["POST"])
def delete_song_from_playlist(playlist_id, playlist_track_id):
    """Delete song from playlist"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    playlist_track = PlaylistTracks.query.get_or_404(playlist_track_id)

    if playlist_track.playlist_id != playlist_id:
        raise Unauthorized()

    db.session.delete(playlist_track)
    db.session.commit()

    flash("Song deleted!", "success")
    return redirect(url_for("show_playlist", playlist_id=playlist_id))

######################
# SONG ROUTES
######################


@app.route("/songs/<string:spotify_id>")
def show_song_details(spotify_id):
    """Show song details"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    song_info = get_song_info(token, spotify_id)

    return render_template("song_details.html", song_info=song_info)


######## things to potentially add##########

# block menu bar.
# have login/signup be one link
# use draw.io to make a diagram of the app


# https://app.diagrams.net
