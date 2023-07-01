from flask import Blueprint, flash, request, jsonify, json, session
from flask import redirect, render_template, url_for
from forms import MapListForm, CreateMapForm
from models import db, Funcionario, Loja, Secção, Mapa, Produto, Marcador, Expositor, ConteudoExpositor
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
        maps = db.session.query(Mapa, Funcionario).filter(Mapa.loja_id==active_user.loja_id, Mapa.funcionario_id ==Funcionario.id).all()

        if maps:
            if request.method == 'POST':
                idmap = form.mapId.data
                session['map'] = idmap

                print(idmap)

                return redirect('/EditMap')

        return render_template("ListagemMapas.html", title = "MapList", formFront = form, active_user = employee, mapsList = maps)
    else:
        return redirect('/login')

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


        # fazer um ciclo for para cada um dos de cimas onda da add a bd e depois no fim dá commit
        # testando solução com um dict 
        # para depois implementar a serio

        if request.method == 'POST':
            mapa = json.loads(createForm.map.data)

            # ober numero de textos
            numLabels = mapa[0]['numLabels']
            # ober numero de textos
            numExpos = mapa[0]['numExpos']

            new_Map= Mapa(comprimento = mapa[0]['width'], altura = mapa[0]['height'], funcionario_id = active_user.id, loja_id = active_user.loja_id)    
            db.session.add(new_Map)
            db.session.commit()

            # ir buscar o ultimo mapa a ser criado nesta loja por este funcionario, para utilizar nos commits
            lastMapa = db.session.query(Mapa).filter(Mapa.funcionario_id==active_user.id, Mapa.loja_id == active_user.loja_id).order_by(Mapa.id.desc()).first()
            
            if(numLabels != 0):
                for element in mapa[1+numExpos:]:
                    print(element)
                    lastMapa = db.session.query(Mapa).filter(Mapa.funcionario_id==active_user.id, Mapa.loja_id == active_user.loja_id).order_by(Mapa.id.desc()).first()
                    new_marker = Marcador(mapa_id = lastMapa.id, angulo = element['angle'], coordenadaX = element['posX'], coordenadaY = element['posY'], texto = element['value'])
                    db.session.add(new_marker)
                    db.session.commit()
                    
                    
            for element in mapa[1:numLabels+1]:
                    new_expo = Expositor(capacidade = element['capacity'], divisorias = element['divisions'], coordenadaX = element['posX'], coordenadaY = element['posY'],
                                        comprimento = element['width'], altura = element['height'], secção_id = element['storeSection'], mapa_id = lastMapa.id)
                    db.session.add(new_expo)
                    db.session.commit()

                    # ir buscar o ultimo expo a ser criado neste mapa para utilizar na tabela do ConteudoExpositor
                    lastExpo = db.session.query(Expositor).filter(Expositor.secção_id == element['storeSection'], Expositor.mapa_id == lastMapa.id).order_by(Expositor.id.desc()).first()
            
                    if(element['products'] != ''):
                        listConteudoExpositor  = ['produto1_id', 'produto2_id', 'produto3_id','produto4_id','produto5_id', 'produto6_id']
                        new_expoContent = ConteudoExpositor( Expositor_id = lastExpo.id)

                        for i, product in enumerate(listConteudoExpositor):
                            if i < len(element['products']):
                                setattr(new_expoContent, f"produto{i+1}_id", element['products'][i])
                            else:
                                setattr(new_expoContent, f"produto{i+1}_id", None)
                        db.session.add(new_expoContent)
                    db.session.commit()

            return redirect('/MapsList')

    else:
        return redirect('/login')

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
    
    print('hiiiiiiiiiii')
    print(session)

    # fzer queries para obter dados do mapa e mostra-lo no frontend enviando um json
    if session.get('map') is not None:
        map_id = session.get('map')
        
        map = db.session.query(Mapa).filter(Mapa.id==map_id).first()

        print('map.data_registo')
        print(map.data_registo)

    return render_template("EditarMapa.html", title = "EditStoreMap", active_user = employee)