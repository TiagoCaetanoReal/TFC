from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired


class ClienteLoginForm(FlaskForm):
    username_cliente = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_cliente = PasswordField(label="Password", validators=[InputRequired()])
    login = SubmitField(label="Login")


class ClienteRegisterForm(FlaskForm):
    username_cliente = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_cliente = PasswordField(label="Password", validators=[InputRequired()])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_cliente")])
    register = SubmitField(label="Registar")


class ClienteEditForm(FlaskForm):
    username_cliente = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_cliente = PasswordField(label="Password", validators=[InputRequired()])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_cliente")])
    edit = SubmitField(label="Confirmar Alterações")
    goBack = SubmitField(label="goBack")