from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


class FuncionarioLoginForm(FlaskForm):
    username_funcionario = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    login = SubmitField(label="Login")

    
class FuncionarioRegisterForm(FlaskForm):
    username_funcionario = StringField(label="Nome Usuário", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Register = SubmitField(label="Registar")

    
class FuncionarioEditForm(FlaskForm):
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Alter = SubmitField(label="Alterar")

    
class MapListForm(FlaskForm):
    idMap = StringField(label="Inserir número do Mapa", render_kw={"placeholder": "Inserir número do Mapa"})
    print = SubmitField(label="Imprimir Listagem")
    createMap = SubmitField(label="Criar Mapa")
    deleteMap = SubmitField(label="Eliminar")


class CreateProductForm(FlaskForm):
    name = StringField(label="Inserir o Nome do Produto", render_kw={"placeholder": "Baguete"}, validators=[InputRequired(), Length(min=3, max=40)])
    price = StringField(label="Inserir o Preço do Produto", render_kw={"placeholder": "3.50"}, validators=[InputRequired()])
    iva = SelectField(label='Inserir a Percentagem do Iva', coerce=str, validators=[DataRequired()])
    metric = SelectField('Inserir a Unidade de Medida', coerce=str, validators=[DataRequired()])        
    origin = SelectField(label='Inserir a Origem do Produto', coerce=str, validators=[DataRequired()])
    department = SelectField('Inserir a Secção do Produto', coerce=str, validators=[DataRequired()])  
    photoURI = StringField(validators=[InputRequired()])
    photoFile = FileField('Image', validators=[ FileAllowed(['jpg', 'png'], 'Apenas imagens JPG e PNG são permitidas.')])
    createProduct = SubmitField(label="Criar Produto")


class NutritionTableForm(FlaskForm):
    kcal100gr = StringField(validators=())
    kj100gr = StringField()
    lipids100gr = StringField()
    carbohydrates100gr = StringField()
    sugars100gr = StringField()
    fibers100gr = StringField()
    protein100gr = StringField()
    salt100gr = StringField()
    kcalDR = StringField()
    kjDR = StringField()
    lipidsDR = StringField()
    carbohydratesDR = StringField()
    sugarsDR = StringField()
    fibersDR = StringField()
    proteinDR = StringField()
    saltDR = StringField()

    
class ProductsListForm(FlaskForm):
    productId = IntegerField('productID')
    productIdBtn = SubmitField('productIdBtn')