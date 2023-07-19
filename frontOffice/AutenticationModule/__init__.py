from flask import Blueprint, request, session
from flask import redirect, render_template 
from forms import ClienteLoginForm, ClienteRegisterForm, ClienteEditForm, ClienteScanStore
from models import db, Cliente, bcrypt
from flask_login import login_user, logout_user, current_user 

AutenticationClientModule = Blueprint("AutenticationClientModule", __name__)

@AutenticationClientModule.route("/")
def index():
    return redirect("/login")

@AutenticationClientModule.route("/login", methods=['GET', 'POST'])
def doLogin():
    form = ClienteLoginForm()

    if request.method == 'POST':
        if form.validate_on_submit() and form.login.data == True:
            try:
                user = db.session.query(Cliente).filter(Cliente.nome == form.username_cliente.data).first()
                
                if(user == None):
                    form.username_cliente.errors.append("Nome Incorreto")
                else:
                    if(bcrypt.check_password_hash(user.password, form.password_cliente.data)):
                        login_user(user)
                        
                        return redirect('/ScanStore')
                    else:
                        form.password_cliente.errors.append("Palavra-Passe Incorreta")

            except Exception as e:
                return f'Erro ao iniciar sessão: {str(e)}'
            
        elif form.loginGuest.data == True:   
            try:
                user = db.session.query(Cliente).filter(Cliente.id == 0).first() 
                login_user(user)
                
                return redirect('/ScanStore')
                      
            except Exception as e:
                return f'Erro ao iniciar sessão: {str(e)}'
            
    return render_template("LoginClient.html", title = "Login", formFront = form)



@AutenticationClientModule.route("/register", methods=['GET', 'POST'])
def doRegister():
    form = ClienteRegisterForm()
    if request.method == 'POST':
        user = db.session.query(Cliente).filter(Cliente.nome == form.username_cliente.data).first()
        
      
        if form.validate_on_submit() and form.register.data == True:
            encrypted_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('UTF-8')
            
            if(user != None):
                l = list(form.username_cliente.errors)
                l.append("Nome já existe")
                form.username_cliente.errors = tuple(l)
                
            else:
                try:
                    new_user = Cliente(nome=form.username_cliente.data, password =  encrypted_password)

                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/login')
                
                except Exception as e:
                    return f'Erro ao criar conta: {str(e)}'
            
    return render_template("RegisterClient.html", title = "Login", formFront = form)



@AutenticationClientModule.route("/ScanStore", methods=['GET', 'POST'])
def scanStore():
    form = ClienteScanStore()
    active_user = current_user

    if(active_user.is_authenticated):

        if request.method == 'POST':
            
            session['storeID'] = form.storeID.data
            
            return redirect('\Store')
    else:
        return redirect('\login')

    return render_template("QRcode.html", title = "Login", formFront = form)



@AutenticationClientModule.route("/editClient", methods=['GET', 'POST'])
def doAlteration():
    active_user = current_user
    form = ClienteEditForm()
    
    if(active_user.is_authenticated):
        userData = db.session.query(Cliente).filter(Cliente.id == active_user.id).first()

        if(request.method == 'POST'):
            if form.validate_on_submit():
                try:
                    if form.username_cliente.data != '': 
                        if db.session.query(Cliente).filter(Cliente.nome == form.username_cliente.data).first() is None:
                            if form.username_cliente.data != userData.nome:
                                setattr(userData, 'nome', form.username_cliente.data)
                        else:
                            l = list(form.username_cliente.errors)
                            l.append("Utilizador já existe, use outro nome")
                            form.username_cliente.errors = tuple(l)
                                

                    if form.oldPassword_cliente.data != '':                         
                        if bcrypt.check_password_hash(userData.password, form.oldPassword_cliente.data) == True:
                            if form.password_cliente.data != '' and form.confirm_password.data != '' :

                                if(len(form.password_cliente.data) < 5 or len(form.password_cliente.data) > 20):
                                    l = list(form.password.errors)
                                    l.append("Campo deve conter entre 5 e 20 caracteres")
                                    form.password.errors = tuple(l)

                                elif(len(form.confirm_password.data) < 5 or len(form.confirm_password.data) > 20):
                                    l = list(form.confirm_password.errors)
                                    l.append("Campo deve conter entre 5 e 20 caracteres")
                                    form.confirm_password.errors = tuple(l) 
                                
                                if(form.password_cliente.data == form.confirm_password.data): 
                                    encrypted_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('UTF-8')
                                    userData.password = encrypted_password

                            elif form.password_cliente.data == '' :
                                l = list(form.password_cliente.errors)
                                l.append("Campo tem de ser preenchido")
                                form.password_cliente.errors = tuple(l)  

                                if form.confirm_password.data == '' :
                                    l = list(form.confirm_password.errors)
                                    l.append("Campo tem de ser preenchido")
                                    form.confirm_password.errors = tuple(l)    

                        elif(bcrypt.check_password_hash(userData.password, form.oldPassword_cliente.data) != True):
                            l = list(form.oldPassword_cliente.errors)
                            l.append("Palavra-Passe Inválida")
                            form.oldPassword_cliente.errors = tuple(l)    

                    if not form.username_cliente.errors and not form.password_cliente.data and not form.confirm_password.data:
                        db.session.commit()
                        return redirect('/Store')

                except Exception as e:
                    return f'Erro ao salvar o edição: {str(e)}'
        

        return render_template("EditClient.html", title = "Login", formFront = form, username = userData.nome)
    
    else:
        return redirect('\login')
    

@AutenticationClientModule.route('/logout')
def logOut():
   logout_user()
   return redirect('/login')