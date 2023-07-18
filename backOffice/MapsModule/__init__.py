from flask import Blueprint, flash, request, jsonify, json, session
from flask import redirect, render_template, url_for
from forms import MapListForm, CreateMapForm, EditMapForm
from models import db, Funcionario, Loja, Secção, Mapa, Produto, Marcador, Expositor, ConteudoExpositor
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

MapsModule = Blueprint("MapsModule", __name__)


@MapsModule.route("/MapsList", methods=['GET', 'POST'])
def seeMapList():
    form = MapListForm()
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome, active_user.loja_id]

    
    if(active_user.is_authenticated):
        maps = db.session.query(Mapa, Funcionario).filter(Mapa.loja_id==active_user.loja_id, Mapa.eliminado == False, Mapa.funcionario_id == Funcionario.id).all()

        if maps:
            if request.method == 'POST':
                acao = form.action.data

                if(acao == 'Editar'):
                    session['map'] = form.mapId.data

                    return redirect('/EditMap')
                
                elif(acao == 'ChangeMap'):
                    map = db.session.query(Mapa).filter(Mapa.loja_id==active_user.loja_id, Mapa.Usando == True).first()
                    # caso exista uma mapa em uso
                    if map:
                        map.Usando = False
                        db.session.commit()
                    
                    # colocar mapa em uso
                    map = db.session.query(Mapa).filter(Mapa.id == form.mapId.data).first()
                    map.Usando = True
                    db.session.commit()
                    return redirect('/MapsList')
                
                elif(acao == 'deleteMaps'):
                    mapsToDelete = form.mapsToDelet.data.split(",")

                    nested_transaction = db.session.begin_nested()

                    for mapToDelete in mapsToDelete:
                        map = db.session.query(Mapa).filter(Mapa.id == mapToDelete).first()
                        map.eliminado = True

                        exposInMap = db.session.query(Expositor).filter(Expositor.mapa_id == mapToDelete).all()

                        expo_ids = [expo.id for expo in exposInMap]

                        expoContents = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.expositor_id.in_(expo_ids)).all()

                        tagsInMap = db.session.query(Marcador).filter(Marcador.mapa_id == mapToDelete).all()

                        for expo in exposInMap:
                            expo.eliminado = True

                        for expoContent in expoContents:
                            expoContent.eliminado = True

                        for tag in tagsInMap:
                            tag.eliminado = True


                    nested_transaction.commit()
                    db.session.commit()
                    return redirect('/MapsList')



        return render_template("ListagemMapas.html", title = "MapList", formFront = form, active_user = employee, mapsList = maps)
    else:
        return redirect('/login')


@MapsModule.route("/MakeMap", methods=['GET', 'POST'])
def CreateStoreMap():
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
    
    if(active_user.is_authenticated):
        createForm = CreateMapForm() 
         
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

            print(mapa)

            # ober numero de textos
            numLabels = mapa[0]['numLabels']
            # ober numero de textos
            numExpos = mapa[0]['numExpos']

            new_Map= Mapa(comprimento = mapa[0]['width'], altura = mapa[0]['height'], funcionario_id = active_user.id, loja_id = active_user.loja_id)    
            db.session.add(new_Map)
            db.session.commit()

            # ir buscar o ultimo mapa a ser criado nesta loja por este funcionario, para utilizar nos commits
            lastMapa = db.session.query(Mapa).filter(Mapa.funcionario_id==active_user.id, Mapa.loja_id == active_user.loja_id, Mapa.eliminado == 0).order_by(Mapa.id.desc()).first()
            
            if(numLabels != 0):
                for element in mapa[1+numExpos:]:
                    new_marker = Marcador(mapa_id = lastMapa.id, angulo = element['angle'], coordenadaX = element['posX'], coordenadaY = element['posY'], 
                                         comprimento = element['width'], altura = element['height'], texto = element['value'])
                    db.session.add(new_marker)
                    db.session.commit()
                
                
            if(numExpos != 0):    
                    
                for element in mapa[1:numExpos+1]:
                    new_expo = Expositor(capacidade = element['capacity'], divisorias = element['divisions'], coordenadaX = element['posX'], coordenadaY = element['posY'],
                                        comprimento = element['width'], altura = element['height'], secção_id = element['storeSection'], mapa_id = lastMapa.id)
                    db.session.add(new_expo)
                    db.session.commit()

                    # ir buscar o ultimo expo a ser criado neste mapa para utilizar na tabela do ConteudoExpositor
                    lastExpo = db.session.query(Expositor).filter(Expositor.secção_id == element['storeSection'], Expositor.mapa_id == lastMapa.id, Expositor.eliminado == 0).order_by(Expositor.id.desc()).first()
            
                    if(element['products'] != ''):
                        listConteudoExpositor  = ['produto1_id', 'produto2_id', 'produto3_id','produto4_id','produto5_id', 'produto6_id']
                        new_expoContent = ConteudoExpositor( expositor_id = lastExpo.id)

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
    active_user = current_user
    seccao_id = request.args.get('seccaoId')

    productsQuery = db.session.query(Produto).filter(Produto.secção_id == seccao_id, Produto.loja_id == active_user.loja_id).all()

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


    if(active_user.is_authenticated):
        editForm = EditMapForm()

        idmap = session.get('map')

        #query para a secção
        departmentQuery = db.session.query(Secção).all()
        department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
        department_presets_group_list = [(' ',"Selecionar Secção")]


        for department in department_group_list:    
            department_presets_group_list.append(department)

        editForm.departments.choices = department_presets_group_list


        # fazer um ciclo for para cada um dos de cimas onda da add a bd e depois no fim dá commit
        # testando solução com um dict 
        # para depois implementar a serio

        if request.method == 'POST':
            mapa = json.loads(editForm.map.data) 

            # ober numero de textos
            numLabels = mapa[0]['numLabels']
            # ober numero de textos
            numExpos = mapa[0]['numExpos']

            # ___________________________________working_______________________________________________ 
            # apartir das tag na db ver quais foram alteradas/removidas e adicionadas
            if(numLabels != 0):
                listLabelsTag = ['coordenadaX','coordenadaY','comprimento','altura','angulo','texto']
                tags = db.session.query(Marcador).filter(Marcador.mapa_id == idmap, Marcador.eliminado == 0).all()
                    
                # Obtenha os IDs dos marcadores existentes
                ids_tags = [tag.id for tag in tags]

                editedTag = []
                
                ####################################################
                # verifica se existem tags novas/eliminadas ou modificadas
                for element in mapa[1+numExpos:]:
                    # verifica se a tags eliminadas ou modificadas
                    if element['id'] in ids_tags:
                        editedTag.append(element['id'])

                        modifiedTag = db.session.query(Marcador).filter(Marcador.id == element['id'], Marcador.eliminado == 0).first()
                        
                        for index, field in enumerate(element):
                            if index  > 0:
                                valor = listLabelsTag[index-1]

                                if str(element[field]) != str(getattr(modifiedTag, valor)):
                                    setattr(modifiedTag, valor, element[field])
                        
                    
                    # verifica se existem tags novas
                    else:
                        editedTag.append(element['id'])
                    
                    db.session.commit()  
                ####################################################

                # tentar verificar pelos ids quais as tag que existem ainda e que foram adicionadas
                
                ####################################################
                # se existirem novos arcadores, estes são adicionados á db
                newTags = [x for x in editedTag if x not in ids_tags]

                if newTags:
                    for element in mapa[1+numExpos:]:
                        for tag in newTags:
                            if element['id'] == tag:
                                new_marker = Marcador(mapa_id = idmap, angulo = element['angle'], coordenadaX = element['posX'], coordenadaY = element['posY'], 
                                                        comprimento = element['width'], altura = element['height'], texto = element['value'])
                                db.session.add(new_marker)
                    db.session.commit()
                ####################################################


                ####################################################
                # se existirem marcadores removidos
                ids_tags = [x for x in ids_tags if x not in editedTag]

                if ids_tags:
                    for tag in ids_tags:
                        deletedTag = db.session.query(Marcador).filter(Marcador.id == tag, Marcador.eliminado == 0).first()
                        deletedTag.eliminado = True
                    db.session.commit()
                ####################################################

            #tentar guardar dados novos dos mesmo elementos
            #^ter cuidado com aqueles que são apagados, ver se id existe caso contrario fazer delete
            if(numLabels != 0):
                listLabelsTag = ['coordenadaX','coordenadaY','comprimento','altura','angulo','texto']

                for element in mapa[1+numExpos:]:
                    
                    lastMapa = db.session.query(Mapa).filter(Mapa.funcionario_id==active_user.id, Mapa.loja_id == active_user.loja_id, Mapa.eliminado == 0).order_by(Mapa.id.desc()).first()
                    new_marker = Marcador(mapa_id = idmap, angulo = element['angle'], coordenadaX = element['posX'], coordenadaY = element['posY'], 
                                         comprimento = element['width'], altura = element['height'], texto = element['value'])
                    
                    db.session.commit()
            #####################################################################################################################

            if(numExpos != 0):
                listLabelsExpositor  = ['coordenadaX', 'coordenadaY', 'comprimento', 'altura','capacidade', 'divisorias',  'secção_id']
                listConteudoExpositor  = ['produto1_id', 'produto2_id', 'produto3_id','produto4_id','produto5_id', 'produto6_id']

                expos = db.session.query(Expositor).filter(Expositor.mapa_id == idmap, Expositor.eliminado == 0).all()
                ids_expos = [expo.id for expo in expos]

                editedExpos = []
                ####################################################
                # verifica se existem expos novos/eliminados ou modificados
                for element in mapa[1:numExpos+1]:  

                    # guarda e processa os expos modificados
                    if element['id'] in ids_expos:

                        editedExpos.append(element['id'])

                        modifiedExpo = db.session.query(Expositor).filter(Expositor.id == element['id'], Expositor.eliminado == 0).first()
                        
                        for index, field in enumerate(element):

                            if index  > 0 and index < 5:
                                valor = listLabelsExpositor[index-1]

                                if str(element[field]) != str(getattr(modifiedExpo, valor)):
                                    setattr(modifiedExpo, valor, element[field])
                                
                            elif index == 5:
                                
                                modifiedExpoContent = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.expositor_id == element['id'], ConteudoExpositor.eliminado == 0).first()

                                for index, product in enumerate(element[field]):
                                    valorProduct = listConteudoExpositor[index]

                                    if str(product) != str(getattr(modifiedExpoContent, valorProduct)):
                                        setattr(modifiedExpoContent, valorProduct, product)

                            elif index  > 5 and index < 9:
                                valor = listLabelsExpositor[index-2]

                                if str(element[field]) != str(getattr(modifiedExpo, valor)):
                                    setattr(modifiedExpo, valor, element[field])
                            
                    # guarda os expos novos
                    else:
                        editedExpos.append(element['id'])
                    
                    db.session.commit()  
                ####################################################


                newExpos = [x for x in editedExpos if x not in ids_expos]
                newExpoIds = []
                    

                if newExpos:
                    for element in mapa[1:numExpos+1]:
                        for expo in newExpos:
                            if element['id'] == expo:
                                # cria o novo expo
                                new_expo = Expositor(capacidade = element['capacity'], divisorias = element['divisions'], coordenadaX = element['posX'], coordenadaY = element['posY'],
                                        comprimento = element['width'], altura = element['height'], secção_id = element['storeSection'], mapa_id = idmap)
                                db.session.add(new_expo)
                                db.session.commit()
                                # procura o expo acabado de criar para utilizar na criação dp conteudoExpositor
                                lastExpo = db.session.query(Expositor).filter(Expositor.mapa_id == idmap).order_by(Expositor.id.desc()).first()
                              
                                # 
                                if lastExpo: 
                                    # armazena o id dos novos expos
                                    newExpoIds.append(lastExpo.id)
                            
                        for newExpoId in newExpoIds:
                            if(element['products'] != ''):    
                                new_expoContent = ConteudoExpositor( expositor_id = newExpoId)

                                for i, product in enumerate(listConteudoExpositor):
                                    if i < len(element['products']):
                                        setattr(new_expoContent, f"produto{i+1}_id", element['products'][i])
                                    else:
                                        setattr(new_expoContent, f"produto{i+1}_id", None)
                                db.session.add(new_expoContent)
                               
                            db.session.commit()


            # ####################################################
            # # se existirem expositores e conteudoExpo removidos
                ids_expos = [x for x in ids_expos if x not in editedExpos] 

                if ids_expos:
                    for id in ids_expos:
                        deletedExpo= db.session.query(Expositor).filter(Expositor.id == id, Expositor.eliminado == 0).first()
                        deletedExpo.eliminado = True
                        
                        deletedContent = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.expositor_id == id, ConteudoExpositor.eliminado == 0).first()
                        deletedContent.eliminado = True
                    db.session.commit()
            ####################################################

            return redirect('/MapsList')

    else:
        return redirect('/login')
    
    
    return render_template("EditarMapa.html", title = "EditStoreMap", active_user = employee, editFormFront = editForm)
    


@MapsModule.route("/fetchMap", methods=['GET','POST'])
def fetchMap():

    # fzer queries para obter dados do mapa e mostra-lo no frontend enviando um json
    if session.get('map') is not None:
        map_id = session.get('map')
        mapDictList = []
        
        map = db.session.query(Mapa).filter(Mapa.id==map_id).first()

        expos = db.session.query(Expositor).filter(Expositor.mapa_id == map_id, Expositor.eliminado == 0).all()
        tags = db.session.query(Marcador).filter(Marcador.mapa_id == map_id, Marcador.eliminado == 0).all()

        mapDictList.append({"width": float(map.comprimento), "height": float(map.altura), "numExpos": len(expos), "numLabels": len(tags)})

        for expo in expos:
            produtos = []
            conteudoExpositores = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.expositor_id == expo.id, ConteudoExpositor.eliminado == 0).first()
            for index in range(expo.capacidade):
                produtos.append(getattr(conteudoExpositores, f"produto{index+1}_id"))

            colorQuery = db.session.query(Secção).filter(Secção.id==expo.secção_id).first()
            
            mapDictList.append({"id": expo.id, "posX": float(expo.coordenadaX), "posY": float(expo.coordenadaY), "width": float(expo.comprimento),
                            "height": float(expo.altura), "color": colorQuery.cor, "products": produtos, 
                            "capacity": expo.capacidade, "divisions": expo.divisorias, 
                            "storeSection": expo.secção_id, "storeSectionColor": colorQuery.cor})

        for tag in tags:
            mapDictList.append( {"id": tag.id, "posX": float(tag.coordenadaX), "posY": float(tag.coordenadaY), "width": float(tag.comprimento),
                                "height": float(tag.altura), "angle": tag.angulo, "value": tag.texto})
         
    return jsonify(mapDictList)