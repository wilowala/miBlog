from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,TextAreaField, SubmitField,ValidationError, EmailField
from wtforms.validators import DataRequired,Email
from flask_login import current_user
from ..models import User

class UpdateProfile(FlaskForm):
    username = StringField('Enter Your Username', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(),Email()])
    bio = TextAreaField('Write a brief bio about you.',validators = [DataRequired()])
    profile_picture = FileField('profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError("The Email has already been taken!")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username = username.data).first():
                raise ValidationError("The username has already been taken")

class CreatePost(FlaskForm):
    heading = StringField('Title',validators=[DataRequired()])
    body = TextAreaField('Blog Content',validators=[DataRequired()])
    submit = SubmitField('Post')

class ContactForm(FlaskForm):
    name = StringField('Enter Your Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(),Email()])
    message = TextAreaField('Write your message.',validators = [DataRequired()])
    submit = SubmitField('Submit')