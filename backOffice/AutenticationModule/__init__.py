from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm, FuncionarioRegisterForm, FuncionarioEditForm
from models import db, Funcionario, Loja, Secção
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

AutenticationModule = Blueprint("AutenticationModule", __name__)

@AutenticationModule.route("/")
def index():
    return redirect("/editEmployee")


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

    storeQuery = db.session.query(Loja).all()
    store_group_list=[(str(i.id), i.nome) for i in storeQuery]
    store_presets_group_list = [(' ',"Selecionar Loja"), ('0',"Quinta do Conde, Avenida 1")]

    for store in store_group_list:    
        store_presets_group_list.append(store)

    departmentQuery = db.session.query(Secção).all()
    department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
    department_presets_group_list = [(' ',"Selecionar Secção"), ('0',"Talho")]
   
   
    for department in department_group_list:    
        department_presets_group_list.append(department)

            
    form.store.choices = store_presets_group_list
    form.department.choices = department_presets_group_list

    return render_template("RegisterFunc.html", title = "Login", formFront = form)


@AutenticationModule.route("/editEmployee", methods=['GET', 'POST'])
def doAlteration():
    form = FuncionarioEditForm()

    storeQuery = db.session.query(Loja).all()
    store_group_list=[(str(i.id), i.nome) for i in storeQuery]
    store_presets_group_list = [(' ',"Selecionar Loja"), ('0',"Quinta do Conde, Avenida 1")]

    for store in store_group_list:    
        store_presets_group_list.append(store)

    departmentQuery = db.session.query(Secção).all()
    department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
    department_presets_group_list = [(' ',"Selecionar Secção"), ('0',"Talho")]
   
   
    for department in department_group_list:    
        department_presets_group_list.append(department)

            
    form.store.choices = store_presets_group_list
    form.department.choices = department_presets_group_list

    return render_template("EditarFunc.html", title = "Login", formFront = form)