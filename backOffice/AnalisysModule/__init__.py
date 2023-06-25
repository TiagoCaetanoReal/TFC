from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm
from models import db, Funcionario, Loja, Secção, Mapa
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

AnalisysModule = Blueprint("AnalisysModule", __name__)


@AnalisysModule.route("/ProductsTable", methods=['GET', 'POST'])
def seeProductsTable():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]

    return render_template("ConsultarProdutos.html", title = "ProductsTable", active_user = employee)




@AnalisysModule.route("/ExhibitorsTable", methods=['GET', 'POST'])
def seeExhibitorsTable():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]

    return render_template("ConsultarExpositor.html", title = "ExhibitorsTable", active_user = employee)