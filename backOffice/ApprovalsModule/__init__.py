from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm
from models import db, Funcionario, Loja, Secção, Mapa
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

ApprovalsModule = Blueprint("ApprovalsModule", __name__)


@ApprovalsModule.route("/ApproveMaps", methods=['GET', 'POST'])
def approveMapList():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]

    return render_template("AprovarMapa.html", title = "ApproveMaps", active_user = employee)



@ApprovalsModule.route("/ApproveEmployees", methods=['GET', 'POST'])
def approveEmployeesList():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
    
    return render_template("AprovarFuncionario.html", title = "ApproveEmployees", active_user = employee)
