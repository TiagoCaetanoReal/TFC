from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm, FuncionarioRegisterForm, FuncionarioEditForm
from models import db, Funcionario, Loja, Secção
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

AutenticationModule = Blueprint("AutenticationModule", __name__)

@AutenticationModule.route("/")
def index():
    return redirect("/login")


@AutenticationModule.route("/login", methods=['GET', 'POST'])
def doLogin():
    form = FuncionarioLoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(Funcionario).filter(Funcionario.nome == form.username_funcionario.data).first()
            if(user == None):
                l = list(form.username_funcionario.errors)
                l.append("Nome de Funcionario Incorreto")
                form.username_funcionario.errors = tuple(l)
            else:
                if(user.password == form.password_funcionario.data):
                    login_user(user)
                    print(current_user.id)
                    return redirect('MapsList')
                else:
                    l = list(form.password_funcionario.errors)
                    l.append("Incorrect Password")
                    form.password_funcionario.errors = tuple(l)

    return render_template("LoginFunc.html", title = "Login", formFront = form)


@AutenticationModule.route("/register", methods=['GET', 'POST'])
def doRegister():
    form = FuncionarioRegisterForm()

    storeQuery = db.session.query(Loja).all()
    store_group_list=[(str(i.id), i.nome+', '+i.morada+', '+i.cidade) for i in storeQuery]
    store_presets_group_list = [(' ',"Selecionar Loja")]

    for store in store_group_list:    
        store_presets_group_list.append(store)

    departmentQuery = db.session.query(Secção).all()
    department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
    department_presets_group_list = [(' ',"Selecionar Secção")]
   
   
    for department in department_group_list:    
        department_presets_group_list.append(department)

            
    form.store.choices = store_presets_group_list
    form.department.choices = department_presets_group_list



    if request.method == 'POST':
        print(form.validate_on_submit())
        print(form.Register.data)
        # if a dar problema
        if form.validate_on_submit() and form.Register.data == True:
            verifyEmploeeName = db.session.query(Funcionario).filter(Funcionario.nome == form.username_funcionario.data).first()

            # encrypted_password = bcrypt.generate_password_hash(form.password_funcionario.data).decode('UTF-8')
             

            if verifyEmploeeName == None:
                try:
                    new_user = Funcionario(nome=form.username_funcionario.data, password =  form.password_funcionario.data , loja_id = form.store.data , secção_id =  form.department.data, cargo = "Funcionário Base",EsperaAprovação = True,Aprovado = False)

                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/login')
                except:
                    return 'error'

    elif request.method == 'GET': 
        return render_template("RegisterFunc.html", title = "Registar", formFront = form)


    return render_template("RegisterFunc.html", title = "Registar", formFront = form)


@AutenticationModule.route("/editEmployee", methods=['GET', 'POST'])
def doAlteration():
    form = FuncionarioEditForm()

    storeQuery = db.session.query(Loja).all()
    store_group_list=[(str(i.id), i.nome+', '+i.morada+', '+i.cidade) for i in storeQuery]
    store_presets_group_list = [(' ',"Selecionar Loja")]

    for store in store_group_list:    
        store_presets_group_list.append(store)

    departmentQuery = db.session.query(Secção).all()
    department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
    department_presets_group_list = [(' ',"Selecionar Secção")]
   
   
    for department in department_group_list:    
        department_presets_group_list.append(department)

            
    form.store.choices = store_presets_group_list
    form.department.choices = department_presets_group_list

    return render_template("EditarFunc.html", title = "Login", formFront = form)