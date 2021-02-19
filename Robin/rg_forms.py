from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, BooleanField, DateField, DateTimeField, SelectField
from wtforms.validators import Required
import time
from datetime import datetime, date, time, timedelta

# class SignUpForm(FlaskForm):
#     username = StringField('Username')
#     password = PasswordField('Password')
#     submit = SubmitField('Sign up')

class NameForm(FlaskForm):
 
    ID = IntegerField('ID des Prüfers', validators=[Required()])
    name = StringField('What is your name?')
    mängel = TextAreaField('Mängel')
    accept = BooleanField('Gerät bestanden')
    date1 = DateTimeField(
        'Datum', format="%Y-%m-%d %H:%M:%S",
        default=datetime.today,
        validators=[Required()])
    date2 = DateField('nächstes Prüfdatum', format="%Y-%m-%d %H:%M:%S",
        default=datetime.now() + timedelta(days=365),
        validators=[Required()])
    submit = SubmitField('Submit')
    

class articleForm(FlaskForm):
    Artikelnummer = StringField('Artikelnummer', validators=[Required()])
    submit = SubmitField('Submit')

class choiceform(FlaskForm):

    System = SelectField(u'ERP System', choices=[('weclapp', 'weclapp'), ('dynamics', 'Dynamics'), ('xentral', 'Xentral'), ('myfactory', 'Myfactory')])
    submit = SubmitField('Submit')

class erpformweclapp(FlaskForm):
    URL = StringField('url', validators=[Required()])
    Password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')

class erpformdynamics(FlaskForm):
    Username = StringField('username', validators=[Required()])
    Password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')

class erpformxentral(FlaskForm):
    URL = StringField('url', validators=[Required()])
    Password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')

class erpformmyfactory(FlaskForm):
    URL = StringField('url', validators=[Required()])
    Password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')   