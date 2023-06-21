from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import ClienteLoginForm, ClienteRegisterForm, ClienteEditForm
from models import db, Funcionario, Loja, Secção
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

AutenticationModule = Blueprint("AutenticationModule", __name__)

@AutenticationModule.route("/")
def index():
    return redirect("/login")


@AutenticationModule.route("/login", methods=['GET', 'POST'])
def doLogin():
    form = ClienteLoginForm()

    return render_template("LogIn.html", title = "Login", formFront = form)


@AutenticationModule.route("/register", methods=['GET', 'POST'])
def doRegister():
    form = ClienteRegisterForm()

    return render_template("Registar.html", title = "Login", formFront = form)


@AutenticationModule.route("/editClient", methods=['GET', 'POST'])
def doAlteration():
    form = ClienteEditForm()

    return render_template("editarPerfil.html", title = "Login", formFront = form)


@AutenticationModule.route("/ScanStore", methods=['GET', 'POST'])
def scanStore():
    form = ClienteEditForm()

    return render_template("QRcode.html", title = "Login", formFront = form)