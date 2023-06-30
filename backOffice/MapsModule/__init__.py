from flask import Blueprint, flash, request, jsonify, json
from flask import redirect, render_template, url_for
from forms import MapListForm, CreateMapForm
from models import db, Funcionario, Loja, Secção, Mapa, Produto
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

MapsModule = Blueprint("MapsModule", __name__)


@MapsModule.route("/MapsList", methods=['GET', 'POST'])
def seeMapList():
    form = MapListForm()
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
    
    if(active_user.is_authenticated):
        data = [
                ['1', 'ferdinade', '22-54-2244'],
                ['2', 'alo', '24-54-2244'],
                ['3', 'bread', '4-54-2244'],
                ['4', 'pão', '25-54-2244']
            ]

        return render_template("ListagemMapas.html", title = "MapList", formFront = form, active_user = employee, data = data)

@MapsModule.route("/FilteredList", methods=['GET', 'POST'])
def FilteredList():
    value = request.form.get('value')

    # Processar os dados correspondentes com base no valor recebido

    # Exemplo: retornar uma lista de dados
    data = [
        ['Nome 1', 'Descrição 1'],
        ['Nome 2', 'Descrição 2']
    ]

    return jsonify(data)

@MapsModule.route("/MakeMap", methods=['GET', 'POST'])
def CreateStoreMap():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
    
    if(active_user.is_authenticated):
        createForm = CreateMapForm()


        #query para a secção
        departmentQuery = db.session.query(Secção).all()
        department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
        department_presets_group_list = [(' ',"Selecionar Secção")]


        for department in department_group_list:    
            department_presets_group_list.append(department)

        createForm.departments.choices = department_presets_group_list

        print("bread")
        if request.method == 'POST':
            print("hi")
            print(createForm.map.data)

            mapa = json.loads(createForm.map.data)

            # ober numero de expos
            numExpos = mapa[0]['numExpos']

            # ober numero de textos
            numLabels = mapa[0]['numLabels']

            # adicionar a ambas as tabelas mapa, expo as dimenssões destes
            # verificar se esta a guarda o id da secção
            # fazer um ciclo for para cada um dos de cimas onda da add a bd e depois no fim dá commit

            print(numExpos)

            # const numExpos = array[0].numExpos;
            # let index = 0
            # array.shift();

            # array.forEach(element => {
            #     if(index < numExpos){
            #         console.log(element);
            #         if(element.storeSection === 0){
            #             canvas.addExpositores(new Expositor(element.id, element.posX , element.posY , element.width, element.height, element.color.toString()));
            #             console.log(canvas.getShapes());
            #         }
            #         else{
            #             canvas.addExpositores(new Expositor(element.id, element.posX, element.posY,  element.width, element.height, element.color.toString(), 
            #                 element.products, element.capacity, element.divisions, element.storeSection, element.storeSectionColor.toString())); 
                            
            #             console.log(canvas.getShapes());
            #         }
            #     }
            # else{
            #         canvas.addTextBlock(new TextBlock(element.id, element.posX, element.posY, element.value, element.angle));
            # }
            # index++;
            # });
    
    else:
        return redirect('/login')


    #   departments = SelectField('Secção do Produto', coerce=str)  
    # products = SelectField('Produtos', coerce=str)  
    # map = SelectField('Produtos', coerce=str)  
    # createMap = SubmitField(label="Criar Mapa")

    return render_template("CriarMapa.html", title = "MakeStoreMap", active_user = employee, createFormFront = createForm)


@MapsModule.route("/fetchColor", methods=['GET','POST'])
def fetchSectionColor():
    # Obter o seccaoId dos parâmetros da solicitação
    seccao_id = request.args.get('seccaoId')

    departmentColorQuery = db.session.query(Secção).filter(Secção.id == seccao_id).first()

    cor = departmentColorQuery.cor

    # Retorne a cor como resposta em formato JSON
    return jsonify({'cor': cor})


@MapsModule.route("/fetchProducts", methods=['GET','POST'])
def fetchProducts():
    seccao_id = request.args.get('seccaoId')

    productsQuery = db.session.query(Produto).filter(Produto.secção_id == seccao_id).all()

    products = [
        {"id": str(product.id), "nome": product.nome}
        for product in productsQuery
    ]

    # Retorne os produtos como resposta em formato JSON
    return jsonify({'products': products})



@MapsModule.route("/EditMap", methods=['GET', 'POST'])
def AlterStoreMap():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]

    return render_template("EditarMapa.html", title = "EditStoreMap", active_user = employee)