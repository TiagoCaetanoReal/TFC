from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired


class FuncionarioLoginForm(FlaskForm):
    username_funcionario = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired()])
    login = SubmitField(label="Login")

    
class FuncionarioRegisterForm(FlaskForm):
    username_funcionario = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired()])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Register = SubmitField(label="Registar")

    
class FuncionarioEditForm(FlaskForm):
    password_funcionario = PasswordField(label="Password", validators=[InputRequired()])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Alter = SubmitField(label="Alterar")