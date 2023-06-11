from flask import Flask
from models import db, Funcionario
from flask_login import LoginManager

from AutenticationModule import AutenticationModule

def create_app(config_filename):
	app = Flask(__name__)
	app.config.from_object(config_filename)
	
	db.init_app(app)

	with app.app_context():
		db.create_all()

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return Funcionario.query.get(int(user_id))

	app.register_blueprint(AutenticationModule)

	return app

if __name__ == "__main__":
	app = create_app("config.DevelopmentConfig")
	app.run(debug=True)