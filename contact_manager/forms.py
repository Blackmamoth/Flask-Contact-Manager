from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Regexp
from contact_manager.models import User, Contact
from flask_login import current_user

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken, please use a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already taken, please use a different one.")


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ContactCreationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    submit = SubmitField('Create Contact')

    def validate_name(self, name):
        contacts = current_user.contacts
        for contact in contacts:
            if contact.name == name.data:
                raise ValidationError("You already have a contact with this name, choose a different name for this contact")

    def validate_email(self, email):
        contacts = current_user.contacts
        for contact in contacts:
            if contact.email == email.data:
                raise ValidationError("You already have a contact with this email, choose a different email for this contact")

    def validate_phone(self, phone):
        if not int(phone.data):
            raise ValidationError("Phone must only contain integers")
        if len(str(phone.data)) < 10 or len(str(phone.data)) > 10:
            raise ValidationError("Phone number must contain 10 digits only")
        contacts = current_user.contacts
        for contact in contacts:
            if contact.phone == phone.data:
                raise ValidationError("You already have a contact with this phone number, choose a different phone for this contact")

class UpdateContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update Contact')

    def validate_phone(self, phone):
        if not int(phone.data):
            raise ValidationError("Phone must only contain integers")
        if len(str(phone.data)) < 10 or len(str(phone.data)) > 10:
            raise ValidationError("Phone number must contain 10 digits only")
