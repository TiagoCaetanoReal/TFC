from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired
from flask_wtf.file import FileField, FileAllowed

class FuncionarioLoginForm(FlaskForm):
    username_funcionario = StringField(label="Nome Utilizador", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    login = SubmitField(label="Login")

    
class FuncionarioRegisterForm(FlaskForm):
    username_funcionario = StringField(label="Nome Utilizador", validators=[InputRequired(), Length(min=5, max=40)])
    password_funcionario = PasswordField(label="Password", validators=[InputRequired(), Length(min=5, max=40)])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    Register = SubmitField(label="Registar")

    
class FuncionarioEditForm(FlaskForm):
    oldPassword_funcionario = PasswordField(label="Password Antiga")
    password_funcionario = PasswordField(label="Password Nova")
    confirm_password = PasswordField(label="Confirmar Password", validators=[ EqualTo("password_funcionario")])
    store = SelectField('Loja', coerce=str, validators=[InputRequired()])
    department = SelectField('Secção', coerce=str, validators=[InputRequired()])
    alter = SubmitField(label="Alterar")
    discard = SubmitField(label="Descartar")


class CreateProductForm(FlaskForm):
    name = StringField(label="Inserir o Nome do Produto", render_kw={"placeholder": "Baguete"}, validators=[InputRequired(), Length(min=3, max=40)])
    price = StringField(label="Inserir o Preço do Produto com Iva", render_kw={"placeholder": "3.50"}, validators=[InputRequired()])
    iva = SelectField(label='Inserir a Percentagem do Iva', coerce=str, validators=[DataRequired()])
    metric = SelectField('Inserir a Unidade de Medida', coerce=str, validators=[DataRequired()])        
    origin = SelectField(label='Inserir a Origem do Produto', coerce=str, validators=[DataRequired()])
    department = SelectField('Inserir a Secção do Produto', coerce=str, validators=[DataRequired()])  
    photoURI = StringField(validators=[InputRequired()])
    photoFile = FileField('Image', validators=[ FileAllowed(['jpg', 'png'], 'Apenas imagens JPG e PNG são permitidas.')])
    createProduct = SubmitField(label="Criar Produto")



class EditProductForm(FlaskForm):
    name = StringField(label="Inserir o Nome do Produto", render_kw={"placeholder": "Baguete"}, validators=[InputRequired(), Length(min=3, max=40)])
    price = StringField(label="Inserir o Preço do Produto com Iva", render_kw={"placeholder": "3.50"}, validators=[InputRequired()])
    iva = SelectField(label='Inserir a Percentagem do Iva', coerce=str, validators=[DataRequired()])
    metric = SelectField('Inserir a Unidade de Medida', coerce=str, validators=[DataRequired()])        
    origin = SelectField(label='Inserir a Origem do Produto', coerce=str, validators=[DataRequired()])
    department = SelectField('Inserir a Secção do Produto', coerce=str, validators=[DataRequired()])  
    photoURI = StringField()
    photoFile = FileField('Image', validators=[ FileAllowed(['jpg', 'png'], 'Apenas imagens JPG e PNG são permitidas.')])
    editProduct = SubmitField(label="Alterar Produto")


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
    action = StringField('ação')
    productsToDelet = StringField('productsToDelet')

    department = SelectField('Filtrar por Secção', coerce=str)  

class MapListForm(FlaskForm):
    mapId = IntegerField('mapID')
    action = StringField('ação')
    mapIdBtn = SubmitField('mapIdBtn')
    mapsToDelet = StringField('mapsToDelet')
    print = SubmitField(label="Imprimir Listagem")
    createMap = SubmitField(label="Criar Mapa")
    deleteMap = SubmitField(label="Eliminar")

class CreateMapForm(FlaskForm):
    departments = SelectField('Secção do Produto', coerce=str)  
    products = SelectField('Produtos', coerce=str)  
    map = StringField()  
    createMap = SubmitField(label="Criar Mapa")


class EditMapForm(FlaskForm):
    departments = SelectField('Secção do Produto', coerce=str)  
    products = SelectField('Produtos', coerce=str)  
    map = StringField()  
    editMap = SubmitField(label="Alterar Mapa")


class ClienteLoginForm(FlaskForm):
    username_cliente = StringField(label="Nome Utilizador", validators=[InputRequired(), Length(min=5, max=40)])
    password_cliente = PasswordField(label="Password", validators=[InputRequired()])
    login = SubmitField(label="Login")
    loginGuest = SubmitField(label="Visitante")


class ClienteRegisterForm(FlaskForm):
    username_cliente = StringField(label="Nome Utilizador", validators=[InputRequired(), Length(min=5, max=40)])
    password_cliente = PasswordField(label="Password", validators=[InputRequired()])
    confirm_password = PasswordField(label="Confirmar Password", validators=[InputRequired(), EqualTo("password_cliente")])
    register = SubmitField(label="Registar")


class ClienteEditForm(FlaskForm):
    username_cliente = StringField(label="Nome Utilizador")
    oldPassword_cliente = PasswordField(label="Password Antiga")
    password_cliente = PasswordField(label="Password")
    confirm_password = PasswordField(label="Confirmar Password", validators=[EqualTo("password_cliente")])
    edit = SubmitField(label="Confirmar Alterações")
    goBack = SubmitField(label="goBack")

class ClienteScanStore(FlaskForm):
    storeID =  IntegerField('storeID')
    goToMap = SubmitField(label="Ver Mapa")

class ClienteStoreMap(FlaskForm): 
    searchProduct = StringField("Inserir Produto") 
    expoID =  IntegerField('expoID')
    goToExpo = SubmitField(label="Ver Expositor")
  
class ClienteSearchProduct(FlaskForm): 
    searchProduct = StringField("Inserir Produto")