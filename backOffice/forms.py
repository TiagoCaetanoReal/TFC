from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, DateField, TimeField, Form
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired

class BaseForm(FlaskForm):
    class Meta:
        locales = ['es_ES', 'es']

class FuncionarioLoginForm(BaseForm):
    username_funcionario = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    login = SubmitField(label="Login")

    
class FuncionarioRegisterForm(BaseForm):
    username_funcionario = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Register = SubmitField(label="Registar")

    
class FuncionarioEditForm(BaseForm):
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Alter = SubmitField(label="Alterar")