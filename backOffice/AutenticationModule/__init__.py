from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm, FuncionarioRegisterForm
from models import db, Funcionario
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

AutenticationModule = Blueprint("AutenticationModule", __name__)

@AutenticationModule.route("/")
def index():
    return redirect("/register")


@AutenticationModule.route("/login", methods=['GET', 'POST'])
def doLogin():
    form = FuncionarioLoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            print("bread")
            user = db.session.query(Funcionario).filter(Funcionario.nome == form.username_funcionario.data).first()
            if(user == None):
                l = list(form.username_funcionario.errors)
                l.append("Nome de Funcionario Incorreto")
                form.username_funcionario.errors = tuple(l)
            else:
                if(user.password_funcionario == form.password_funcionario.data):
                    login_user(user)
                    # return redirect('homePage')
                else:
                    l = list(form.password_funcionario.errors)
                    l.append("Incorrect Password")
                    form.password_funcionario.errors = tuple(l)

    return render_template("LoginFunc.html", title = "Login", formFront = form)

@AutenticationModule.route("/register", methods=['GET', 'POST'])
def doRegister():
    form = FuncionarioRegisterForm()
    return render_template("RegisterFunc.html", title = "Login", formFront = form)