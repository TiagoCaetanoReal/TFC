from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm
from models import db, Funcionario, Loja, Secção, Mapa
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

ApprovalsModule = Blueprint("ApprovalsModule", __name__)


@ApprovalsModule.route("/ApproveMapsList", methods=['GET', 'POST'])
def approveMapList():

    return render_template("AprovarMapa.html", title = "ApproveMapsList")