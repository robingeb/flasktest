from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, BooleanField, DateField, DateTimeField
from wtforms.validators import Required

# class SignUpForm(FlaskForm):
#     username = StringField('Username')
#     password = PasswordField('Password')
#     submit = SubmitField('Sign up')

class NameForm(FlaskForm):
 
    ID = IntegerField('ID des Prüfers', validators=[Required()])
    name = StringField('What is your name?')
    mängel = TextAreaField('Mängel')
    accept = BooleanField('Gerät bestanden')
    date1 = DateTimeField('Datum')
    date2 = DateField('Datum')
    submit = SubmitField('Submit')