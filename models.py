from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Cliente(db.Model, UserMixin):
	__tablename__ = 'Cliente' 
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	data_registo = db.Column(db.DateTime, default=datetime.now)

	def __repr__(self) -> str:
		return f"User('{self.nome}',{self.password}','{self.gender}','{self.data_registo}')"


class Loja (db.Model):
    __tablename__= 'Loja'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    cidade = db.Column(db.String(80), unique=True, nullable=False)
    morada = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self) -> str:
        return '<Loja %r>' % self.id  


class Secção (db.Model):
    __tablename__= 'Secção'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25), unique=True, nullable=False)
    cor = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return '<Secção %r>' % self.id   



class Iva (db.Model):
    __tablename__= 'Iva'
    id = db.Column(db.Integer, primary_key=True)
    percentagem = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<Iva %r>' % self.id   


class Foto (db.Model):
    __tablename__= 'Foto'
    id = db.Column(db.Integer, primary_key=True)
    caminhoFot = db.Column(db.String(75), unique=True, nullable=False)

    def __repr__(self) -> str:
        return '<Foto %r>' % self.id   
    

class Origem (db.Model):
    __tablename__= 'Origem'
    id = db.Column(db.Integer, primary_key=True)
    Pais = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self) -> str:
        return '<Origem %r>' % self.id   
    
class Medida(db.Model):
    __tablename__= 'Medida'
    id = db.Column(db.Integer, primary_key=True)
    unMedida = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self) -> str:
        return '<Medida %r>' % self.id   
    

class Produto (db.Model):
    __tablename__= 'Produto'
    id = db.Column(db.Integer, primary_key=True)
    preço = db.Column(db.Integer, unique=False, nullable=False)
    nome = db.Column(db.String(40), unique=False, nullable=False)
    origem_id = db.Column('Origem', db.ForeignKey('Origem.id'), nullable=False)
    origem = db.relationship('Origem', backref='Produto')
    iva_id = db.Column('Iva', db.ForeignKey('Iva.id'), nullable=False)
    iva = db.relationship('Iva', backref='Produto')
    unMedida_id = db.Column('Medida_id', db.ForeignKey('Medida.id'), nullable=False)
    unMedida = db.relationship('Medida', backref='Produto')
    secção_id = db.Column('Secção_id', db.ForeignKey('Secção.id'), nullable=False)
    secção = db.relationship('Secção', backref='Produto')
    loja_id = db.Column('Loja_id', db.ForeignKey('Loja.id'), nullable=False)
    loja = db.relationship('Loja', backref='Produto')
    photoPath = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Produto " + self.nome + " " + str(self.id)
    

class Favorito (db.Model):
    __tablename__= 'Favorito'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column('Produto_id', db.ForeignKey('Produto.id'), nullable=False)
    produto = db.relationship('Produto', backref='Favorito')
    cliente_id = db.Column('Cliente_id', db.ForeignKey('Cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', backref='Favorito')

    def __repr__(self) -> str:
        return '<Favorito %r>' % self.id  
    

class TabelaNutricional100gr (db.Model):
    __tablename__= 'TabelaNutricional100gr'
    id = db.Column(db.Integer, primary_key=True)
    kcal = db.Column(db.Integer, unique=False, nullable=False)
    kj = db.Column(db.Integer, unique=False, nullable=False)
    lipidos = db.Column(db.Integer, unique=False, nullable=False)
    hidratos = db.Column(db.Integer, unique=False, nullable=False)
    fibras = db.Column(db.Integer, unique=False, nullable=False)
    proteinas = db.Column(db.Integer, unique=False, nullable=False)
    açúcares = db.Column(db.Integer, unique=False, nullable=False)
    sal = db.Column(db.Integer, unique=False, nullable=False)
    produto_id = db.Column('Produto_id', db.ForeignKey('Produto.id'), nullable=False)
    produto = db.relationship('Produto', backref='TabelaNutricional100gr')

    def __repr__(self) -> str:
        return '<TabelaNutricional100gr %r>' % self.id  
    

class TabelaNutricionalDR (db.Model):
    __tablename__= 'TabelaNutricionalDR'
    id = db.Column(db.Integer, primary_key=True)
    kcal = db.Column(db.Integer, unique=False, nullable=False)
    kj = db.Column(db.Integer, unique=False, nullable=False)
    lipidos = db.Column(db.Integer, unique=False, nullable=False)
    hidratos = db.Column(db.Integer, unique=False, nullable=False)
    fibras = db.Column(db.Integer, unique=False, nullable=False)
    proteinas = db.Column(db.Integer, unique=False, nullable=False)
    açúcares = db.Column(db.Integer, unique=False, nullable=False)
    sal = db.Column(db.Integer, unique=False, nullable=False)
    produto_id = db.Column('Produto_id', db.ForeignKey('Produto.id'), nullable=False)
    produto = db.relationship('Produto', backref='TabelaNutricionalDR')

    def __repr__(self) -> str:
        return '<TabelaNutricionalDR %r>' % self.id  
    

class Funcionario(db.Model, UserMixin):
    __tablename__ = 'Funcionario'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(40), unique=True) 
    password = db.Column(db.String(60), nullable=False)
    loja_id = db.Column('Loja_id', db.ForeignKey('Loja.id'), nullable=False)
    loja = db.relationship('Loja', backref='Funcionario')
    secção_id = db.Column('Secção_id', db.ForeignKey('Secção.id'), nullable=False)
    secção = db.relationship('Secção', backref='Funcionario')
    cargo = db.Column(db.String(60), nullable=False) 
    EsperaAprovação = db.Column(db.Boolean(), default=True) 
    Aprovado = db.Column(db.Boolean(), default=False) 
    data_registo = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Funcionario " + self.nome + " " + self.cargo
	


class Admin (db.Model,UserMixin):
    __tablename__= 'Admin'
    id =  db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column('Funcionario_id', db.ForeignKey('Funcionario.id'), nullable=False)
    funcionario = db.relationship('Funcionario', backref='Admin')

    def __repr__(self) -> str:
        return '<Admin %r>' % self.id  
    

class Mapa (db.Model):
    __tablename__= 'Mapa'
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column('Funcionario_id', db.ForeignKey('Funcionario.id'), nullable=False)
    funcionario = db.relationship('Funcionario', backref='Mapa') 
    loja_id = db.Column('Loja_id', db.ForeignKey('Loja.id'), nullable=False)
    loja = db.relationship('Loja', backref='Mapa') 
    EsperaAprovação = db.Column(db.Boolean(), default=True) 
    Aprovado = db.Column(db.Boolean(), default=False)
    Usando = db.Column(db.Boolean(), default=False)

    def __repr__(self) -> str:
        return '<Admin %r>' % self.id    


class Expositor (db.Model):
    __tablename__= 'Expositor'
    id = db.Column(db.Integer, primary_key=True)
    capacidade = db.Column(db.Integer, unique=True, nullable=False)
    divisorias = db.Column(db.Integer, unique=True, nullable=False)
    coordenadas = db.Column(db.String(10), unique=True, nullable=False)
    secção_id = db.Column('Secção_id', db.ForeignKey('Secção.id'), nullable=False)
    secção = db.relationship('Secção', backref='Expositor')
    mapa_id = db.Column('Mapa_id', db.ForeignKey('Mapa.id'), nullable=False)
    mapa = db.relationship('Mapa', backref='Expositor')
    produto_id = db.Column('Produto_id', db.ForeignKey('Produto.id'), nullable=False)
    produto = db.relationship('Produto', backref='Expositor')

    def __repr__(self) -> str:
        return '<Admin %r>' % self.id 