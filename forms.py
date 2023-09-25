from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length, URL, Optional


class RegisterForm(FlaskForm):
    """form for registering a user"""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=55)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])
    bio = TextAreaField("Bio", validators=[Optional()])
    profile_image = StringField(
        "Profile Image", validators=[Optional(), URL()])


class LoginForm(FlaskForm):
    """form for logging in a user"""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=55)])


class EditUserForm(FlaskForm):
    """form for editing a user's profile"""

    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])
    bio = TextAreaField("Bio", validators=[Optional()])
    profile_image = StringField(
        "Profile Image", validators=[Optional(), URL()])


class PlaylistForm(FlaskForm):
    """form for creating a playlist"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[InputRequired()])
    image = StringField("Image", validators=[Optional(), URL()])


class SongForm(FlaskForm):
    """form for adding a song to a playlist"""

    song = SelectField("Song", coerce=int)
