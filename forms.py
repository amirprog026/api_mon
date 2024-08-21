from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField,FileField
from wtforms.validators import DataRequired, EqualTo, Length,Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class APIForm(FlaskForm):
    name = StringField('API Name', validators=[DataRequired()])
    endpoint = StringField('Endpoint', validators=[DataRequired()])
    method = SelectField('Method', choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], validators=[DataRequired()])
    description = TextAreaField('Description')
    
    submit = SubmitField('Create API')

class APIRequestForm(FlaskForm):
    request_method = SelectField('Method', choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')])
    body_type = SelectField('Body Type', choices=[('none', 'None'), ('json', 'JSON'), ('form', 'Form Data'), ('file', 'File Upload')])
    headers = TextAreaField('Headers (key=value pairs, one per line)', validators=[Optional(), Length(max=500)])
    request_payload = TextAreaField('JSON Payload', validators=[Optional(), Length(max=500)])
    form_data = TextAreaField('Form Data (key=value pairs, one per line)', validators=[Optional(), Length(max=500)])
    file_upload = FileField('File', validators=[Optional()])
    submit = SubmitField('Send Request')