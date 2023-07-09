from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm, FuncionarioRegisterForm, FuncionarioEditForm
from models import db, Funcionario, Loja, Secção, bcrypt
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

AutenticationFuncModule = Blueprint("AutenticationFuncModule", __name__)

@AutenticationFuncModule.route("/")
def index():
    return redirect("/login")


@AutenticationFuncModule.route("/login", methods=['GET', 'POST'])
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
                if(bcrypt.check_password_hash(user.password, form.password_funcionario.data)):
                    login_user(user)
                    print(current_user.id)
                    return redirect('/MapsList')
                else:
                    l = list(form.password_funcionario.errors)
                    l.append("Incorrect Password")
                    form.password_funcionario.errors = tuple(l)

    return render_template("LoginFunc.html", title = "Login", formFront = form)


@AutenticationFuncModule.route("/register", methods=['GET', 'POST'])
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
        if form.validate_on_submit() and form.Register.data == True:
            verifyEmploeeName = db.session.query(Funcionario).filter(Funcionario.nome == form.username_funcionario.data).first()

            encrypted_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('UTF-8')
             

            if verifyEmploeeName == None:
                try:
                    new_user = Funcionario(nome=form.username_funcionario.data, password =  encrypted_password , loja_id = form.store.data , secção_id =  form.department.data, cargo = "Funcionário Base",EsperaAprovação = True,Aprovado = False)

                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/login')
                
                except Exception as e:
                    return f'Erro ao criar conta: {str(e)}'

    elif request.method == 'GET': 
        return render_template("RegisterFunc.html", title = "Registar", formFront = form)


    return render_template("RegisterFunc.html", title = "Registar", formFront = form)


@AutenticationFuncModule.route("/editEmployee", methods=['GET', 'POST'])
def doAlteration():
    form = FuncionarioEditForm()
    active_user = current_user

    if(active_user.is_authenticated):
        userData = db.session.query(Funcionario).filter(Funcionario.id == active_user.id).first()

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

        if(request.method == 'POST'):
            if form.validate_on_submit():
                try:
                    if(form.oldPassword_funcionario.data != ''): 
                        
                        if bcrypt.check_password_hash(userData.password, form.oldPassword_funcionario.data) == True:
                            if form.password_funcionario.data != '' and form.confirm_password.data != '' :

                                if(len(form.password_funcionario.data) < 5 or len(form.password_funcionario.data) > 20):
                                    form.password.errors.append("Campo deve conter entre 5 e 20 caracteres")

                                elif(len(form.confirm_password.data) < 5 or len(form.confirm_password.data) > 20):
                                    form.password.errors.append("Campo deve conter entre 5 e 20 caracteres")
                                
                                if(form.password_funcionario.data == form.confirm_password.data):
                                    print("FFFFFFFFFFFFFFFFFFFFF")
                                    encrypted_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('UTF-8')
                                    userData.password = encrypted_password
                                    print(encrypted_password)

                            elif form.password_funcionario.data == '' :
                                form.password_funcionario.errors.append("Campo tem de ser preenchido")

                                if form.confirm_password.data == '' :
                                    form.confirm_password.errors.append("Campo tem de ser preenchido")

                                
                        elif(bcrypt.check_password_hash(userData.password, form.oldPassword_funcionario.data) != True):
                            form.oldPassword_funcionario.errors.append("Palavra-Passe Inválida")

                    if form.store.data != userData.loja_id:
                        userData.loja_id = form.store.data

                    if form.department.data != userData.secção_id:
                        userData.secção_id = form.department.data

                    db.session.commit()
                    return redirect('/MapsList')

                except Exception as e:
                    return f'Erro ao salvar o edição: {str(e)}'
        

        return render_template("EditarFunc.html", title = "Login", formFront = form, active_user=active_user)
    
    else:
        return redirect('\login')

# rota para realizar o logout
@AutenticationFuncModule.route('/logout')
def logOut():
   logout_user()
   return redirect('/login')