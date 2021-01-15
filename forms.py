from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField()

class RegisterForm(FlaskForm):
    f_name = StringField("firstName", validators=[DataRequired()])
    s_name = StringField("secondName")
    password = PasswordField("password", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])