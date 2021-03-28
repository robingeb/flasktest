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
    name = StringField('Name des Prüfers')
    mängel = TextAreaField('Mängel')
    accept = BooleanField('Gerät bestanden')
    date1 = DateTimeField(
        'Datum', format="%Y-%m-%d %H:%M:%S",
        default=datetime.today,
        validators=[Required()])
    date2 = DateField('nächstes Prüfdatum', format="%Y-%m-%d %H:%M:%S",
        default=datetime.now() + timedelta(days=365),
        validators=[Required()])
    submit = SubmitField('Bestätigen')
    

class articleForm(FlaskForm):
    Artikelnummer = StringField('Artikelnummer', validators=[Required()])
    submit = SubmitField('Bestätigen')

class choiceform(FlaskForm):

    System = SelectField(u'ERP System', choices=[('weclapp', 'weclapp'), ('dynamics', 'Dynamics'), ('xentral', 'Xentral'), ('myfactory', 'Myfactory')])
    submit = SubmitField('Bestätigen')

class erpformweclapp(FlaskForm):
    URL = StringField('URL', validators=[Required()])
    Password = StringField('API-Key', validators=[Required()])
    submit = SubmitField('Middleware starten')

class erpformdynamics(FlaskForm):
    URL = StringField('URL', validators=[Required()])
    BasicAuth = StringField('BasicAuth', validators=[Required()])
    submit = SubmitField('Middleware starten')

class erpformxentral(FlaskForm):
    URL = StringField('url', validators=[Required()])
    Password = StringField('password', validators=[Required()])
    Username = StringField('Username', validators=[Required()])
    submit = SubmitField('Middleware starten')

class erpformmyfactory(FlaskForm):
    URL = StringField('url', validators=[Required()])
    Password = StringField('password', validators=[Required()])
    Username = StringField('Username', validators=[Required()])
    submit = SubmitField('Middleware starten')   

class articlehomeForm(FlaskForm):
    submit = SubmitField('Prüfbericht')

class choicestartForm(FlaskForm):
    submit = SubmitField('Neue Konfiguration starten')

class choiceendForm(FlaskForm):
    submit = SubmitField('Neue Konfiguration starten')

class choicehomeForm(FlaskForm):
    time = IntegerField('Zeitintervall zwischen Updates', validators=[Required()])
    time_unit = SelectField(u'Zeiteinheit', choices=[('seconds', 'Sekunden'), ('minutes', 'Minuten'), ('hours', 'Stunden'), ('days', 'Tage')], validators=[Required()])
    export = SelectField(u'Anlagen-Export', choices=[('tagid_erp', 'TagIdeasy zu ERP-System'), ('erp_tagid', 'ERP-System zu TagIdeasy'), ('no', 'kein Export')], validators=[Required()])
    submit = SubmitField('Bestätigen')