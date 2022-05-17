from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo
from ..models import User

class SignupForm(FlaskForm):
    username = StringField("Enter username", validators=[DataRequired()])
    email = EmailField("Enter Email", validators=[DataRequired()])
    role = SelectField('Would you like to signup as a writer?', choices=['Yes', 'No'], validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo('password') ])
    submit = SubmitField("Signup")


    def validate_email(self,data_field):
           if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')


class LoginForm(FlaskForm):
     email = EmailField("Enter email", validators=[DataRequired()])
     password = PasswordField('Enter password', validators=[DataRequired()])
     remember = BooleanField('Remember me')
     submit = SubmitField("Login")