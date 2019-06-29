from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Enter Email',validators = [DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email',validators = [DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    password2 = PasswordField('Enter Password Again', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Email already exists')

class QuestionForm(FlaskForm):
    title = StringField('Technology Related', [DataRequired(),Length(min=0, max=50)])
    question = TextAreaField('Type in your query', [DataRequired(), Length(min=10, max=250)])
    tags = StringField('Tags')
    submit = SubmitField('Let The World Answer')

class AnswerForm(FlaskForm):
    answer = TextAreaField('Share your thoughts', [DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Post')
