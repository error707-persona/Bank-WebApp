from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from model.models import Users

class RegisterForm(FlaskForm):

    def validate_username(selfself, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username Already Exists! Please try another username')

    def validate_email(selfself, email_to_check):
        email = Users.query.filter_by(username=email_to_check.data).first()
        if email:
            raise ValidationError('Email Already Exists! Please Try anoother mail')


    username = StringField(label='User Name: ', validators=[Length(min=2, max=30), DataRequired()], )
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class transfer(FlaskForm):
    account = StringField(label='Account No: ')
    bankname = StringField(label='Bank Name: ')
    amount = StringField(label='Amount: ')
    submit = SubmitField(label='Proceed')

class login_pass(FlaskForm):
    account = StringField(label='Account')
    submit = SubmitField(label='Login')


