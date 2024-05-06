from app.model import Profile
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, validators
from wtforms.validators import ValidationError
from flask import flash
from flask_wtf.file import FileAllowed, FileRequired, FileField


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "username"},
    )
    password = PasswordField(
        "Password", validators=[validators.DataRequired()], render_kw={"placeholder": "password"}
    )
    remember_me = BooleanField("Remember me", default=False)


class RegistrationForm(FlaskForm):
    profile_photo = FileField("Profile photo", validators=[
                              FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    name = StringField(label='Name', validators=[
                       validators.DataRequired()], render_kw={"placeholder": "Name"})
    designation = SelectField(label='Designation', choices=[
                              'Student', 'Teacher'])
    contact_no = StringField(
        'Contact No', validators=[validators.Length(min=10, max=10), validators.DataRequired()], render_kw={"placeholder": "Contact Number"})
    email = StringField('email',validators=[validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    username = StringField(
        'username', validators=[validators.DataRequired(), validators.Length(min=4, max=35),validators.Regexp('[a-zA-Z0-9@]',message="Enter valid username")], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[validators.DataRequired(),validators.length(min=4), validators.EqualTo(
        'confirm_password', message='password must match')], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Repeat Password', render_kw={
                                     "placeholder": "Confirm password"})
    accept_toc = BooleanField("I accept the TOC", validators=[
        validators.DataRequired()])

    def validate_username(self, username):
        """
        Validate an email address.

        Parameters:
            email (str): The email address to be validated.

        Raises:
            ValidationError: If the email address is already registered.

        Returns:
            None
        """
        existing_user = Profile.query.filter_by(
            username=username.data).one_or_none()
        if existing_user:
            flash("Username already registered.")
