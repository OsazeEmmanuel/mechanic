from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("login", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                       EqualTo("password", message="Password must match")])
    submit = SubmitField("Register", validators=[DataRequired()])


class MechanicForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = IntegerField("Phone Contact", validators=[DataRequired()])
    address = StringField("Work-shop Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                        EqualTo("password", message="password must match")])
    years_of_experience = IntegerField("Years of Practice", validators=[DataRequired()])
    submit = SubmitField("Register", validators=[DataRequired()])