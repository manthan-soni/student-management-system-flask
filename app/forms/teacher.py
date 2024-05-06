from app.model import Profile
from flask_wtf import FlaskForm
from wtforms import validators, BooleanField, StringField, PasswordField, SelectField, DateField
from wtforms.validators import ValidationError
from flask import flash


class CourseDetails(FlaskForm):
    id = StringField(
        "CourseId",
        validators=[validators.DataRequired()],
        render_kw={'placeholder': "CourseId"},
    )
    name = StringField(
        "Name", validators=[validators.DataRequired()], render_kw={"placeholder": "Course name"}
    )
    description = StringField(
        "Description", validators=[validators.DataRequired()], render_kw={"placeholder": "Course description"}
    )
    start_date = DateField(
        "Start date", validators=[validators.DataRequired()], render_kw={"placeholder": "start date"}
    )
    end_date = DateField(
        "End date", validators=[validators.DataRequired()], render_kw={"placeholder": "end date"}
    )
    link = StringField(
        "Link", validators=[validators.DataRequired()], render_kw={"placeholder": "Course link"}
    )
