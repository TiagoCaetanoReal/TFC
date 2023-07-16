from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from models import db, bcrypt, Funcionario

from backOffice.AutenticationModule import AutenticationFuncModule
from backOffice.MapsModule import MapsModule
from backOffice.ProductsModule import ProductsModule 

def create_app(config_filename):
	app = Flask(__name__)
	app.config.from_object(config_filename)
	
	db.init_app(app)
	bcrypt.init_app(app)

	with app.app_context():
		db.create_all()

	login_manager = LoginManager() 
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return Funcionario.query.get(int(user_id))

	app.register_blueprint(AutenticationFuncModule)
	app.register_blueprint(MapsModule)
	app.register_blueprint(ProductsModule) 

	babel = Babel(app)

	return app

if __name__ == "__main__":
	app = create_app("config.DevelopmentConfig")
	app.run(debug=True)