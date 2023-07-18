from flask import Blueprint, request, session, jsonify
from flask import redirect, render_template
from forms import ClienteSearchProduct, ClienteStoreMap
from models import Favorito, Iva, Medida, Origem, Produto, TabelaNutricional100gr, TabelaNutricionalDR, db,  Mapa, Expositor, Marcador, ConteudoExpositor, Secção
from flask_login import current_user  
from unidecode import unidecode

StoreClientModule = Blueprint("StoreClientModule", __name__)


@StoreClientModule.route("/Store", methods=['GET', 'POST'])
def seeStoreMap():
    form = ClienteStoreMap()
    active_user = current_user
    expo_id = 0

    if(active_user.is_authenticated):

        if request.method == 'POST':  
            # para nao entrar nos resultados de produtos por engano, é usada arestrição seguinte
            # no qual o utilizador tem de inserir algo diferente de vazio e espaço
            if form.searchProduct.data != None and form.searchProduct.data != ' ': 
                session['searchingProduct'] = form.searchProduct.data
                return redirect('/SearchProduct')

            if form.expoID.data != None:
                session['expo'] = form.expoID.data 
                return redirect('/Displayer')

        return render_template("MapPage.html", title = "MapPage", formFront = form, wantedExpo = expo_id, user = active_user)
    else:
        return redirect("/login")
    


@StoreClientModule.route("/fetchMap", methods=['GET','POST'])
def fetchMap(): 
    mapDictList = []
    expo_id = 0
    
    if session.get('wantedExpo') is not None:
        expo_id = session.get('wantedExpo')
        session.pop('wantedExpo')
    
    # fzer queries para obter dados do mapa e mostra-lo no frontend enviando um json
    if session.get('storeID') is not None:
        store_id = session.get('storeID')

        map = db.session.query(Mapa).filter(Mapa.loja_id==store_id, Mapa.Usando == True).first()
        
        session['map'] = map.id 

        expos = db.session.query(Expositor).filter(Expositor.mapa_id == map.id, Expositor.eliminado == False).all()
        tags = db.session.query(Marcador).filter(Marcador.mapa_id ==  map.id, Marcador.eliminado == False).all()

        mapDictList.append({"width": float(map.comprimento), "height": float(map.altura), "numExpos": len(expos), "numLabels": len(tags), "wantedExpo": expo_id})

        for expo in expos:
            produtos = []
            conteudoExpositores = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.expositor_id == expo.id, ConteudoExpositor.eliminado == False).first()
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
             
        return mapDictList
    
    else:
        return redirect('/ScanStore')
    

@StoreClientModule.route("/Displayer", methods=['GET', 'POST'])
def seeDisplayerItems():
    active_user = current_user
    
    if(active_user.is_authenticated):
        idExpo = session.get('expo')  
        products = []
        preferedProducts = []

        expo = db.session.query(Expositor).filter(Expositor.id==idExpo).first()
        department = db.session.query(Secção).filter(Secção.id==expo.secção_id).first() 
        expoContent = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.expositor_id==idExpo).first()

        for index in range(expo.capacidade):
            product = db.session.query(Produto).filter(Produto.id == getattr(expoContent, f"produto{index+1}_id"), Produto.eliminado == 0).first()
            unMedida = db.session.query(Medida).filter(Medida.id == product.unMedida_id).first()
            products.append([product,unMedida])

            prefered = db.session.query(Favorito).filter(Favorito.produto_id == product.id, Favorito.cliente_id == active_user.id, Favorito.eliminado == 0).first()
            
            if prefered:
                preferedProducts.append(prefered)

        return render_template("Expositor.html", title = "ExpoPage", department = department, products = products,  preferedProducts = preferedProducts, user = active_user)
    
    else:
        return redirect("/login")
    
    

@StoreClientModule.route("/fetchProduct", methods=['GET'])
def fetchProduct():
    product_id = request.args.get('idProduto') 
    
    # fzer queries para obter dados do mapa e mostra-lo no frontend enviando um json
    if product_id is not None:
        productDictList = []
        
        product = db.session.query(Produto).filter(Produto.id == product_id).first()
        metric = db.session.query(Medida).filter(Medida.id == product.unMedida_id).first()
        origin = db.session.query(Origem).filter(Origem.id == product.origem_id).first()
        taxes = db.session.query(Iva).filter(Iva.id == product.iva_id).first()

        nutrition100GR = db.session.query(TabelaNutricional100gr).filter(TabelaNutricional100gr.produto_id == product.id).first()
        nutritionDR = db.session.query(TabelaNutricionalDR).filter(TabelaNutricionalDR.produto_id == product.id).first()
        
        productDictList.append([product.nome, product.preço])
        productDictList.append(metric.unMedida)
        productDictList.append(origin.Pais) 
        productDictList.append(taxes.percentagem)

        if nutrition100GR: 
            productDictList.append(["Energia[kcal]", "Energia[kj]", "Lipigos[gr]", "Hidratos carbono[gr]", "Açúcares[gr]", "Fibra[gr]", "Proteínas[gr]", "Sal[gr]"])
            productDictList.append([nutrition100GR.kcal, nutrition100GR.kj,  nutrition100GR.lipidos, nutrition100GR.hidratos, 
                                    nutrition100GR.fibras, nutrition100GR.proteinas, nutrition100GR.açúcares, nutrition100GR.sal])
            productDictList.append([nutritionDR.kcal, nutritionDR.kj, nutritionDR.lipidos, nutritionDR.hidratos, 
                                   nutritionDR.fibras, nutritionDR.proteinas, nutritionDR.açúcares, nutritionDR.sal])
            
        try: 
            return jsonify(productDictList)
        except Exception as e:
                return f'Erro ao enviar dados: {str(e)}'

    
@StoreClientModule.route("/preferedProduct", methods=['GET'])
def preferedProduct():
    active_user = current_user
    product_id = request.args.get('idProduto') 
    
    prefered = db.session.query(Favorito).filter(Favorito.produto_id == product_id, Favorito.cliente_id == active_user.id).first()
    
    if prefered is None:
        new_Favorit = Favorito(produto_id = product_id, cliente_id=active_user.id)
        db.session.add(new_Favorit)

    elif getattr(prefered, 'eliminado'):
        setattr(prefered, 'eliminado', False)
    
    else:
        setattr(prefered, 'eliminado', True)
                            
    db.session.commit()
    
    try: 
        return jsonify(getattr(prefered, 'eliminado'))
    except Exception as e:
            return f'Erro ao enviar dados: {str(e)}'



@StoreClientModule.route("/Favorites", methods=['GET', 'POST'])
def seeFavoritesList():
    active_user = current_user
    store_id = session.get('storeID')

    if(active_user.is_authenticated):

        prefereds = db.session.query(Favorito, Produto, Medida).filter(Favorito.cliente_id == active_user.id, Favorito.eliminado == False, 
                                                                       Produto.loja_id == store_id, Favorito.produto_id  == Produto.id, 
                                                                       Medida.id == Produto.unMedida_id).all()
    

        return render_template("Favoritos.html", title = "FavoritesPage", prefereds = prefereds)
    
    else:
        return redirect("/login")
    

@StoreClientModule.route("/removeFavorite", methods=['GET', 'POST'])
def removeFavorite():  
    prefered_id = request.form['idFavorito']  
    
    prefered = db.session.query(Favorito).filter(Favorito.id == prefered_id).first()
    setattr(prefered, 'eliminado', True)
    db.session.commit()
    
    try: 
        return redirect("/Favorites")
    except Exception as e:
            return f'Erro ao enviar dados: {str(e)}'
    

@StoreClientModule.route("/locateProduct", methods=['GET', 'POST'])
def locateProduct():  
    product_id = request.form['idProduto']  
    map_id = session.get('map')

    expos = db.session.query(Expositor).filter(Expositor.mapa_id == map_id).all()

    wantedExpo = db.session.query(ConteudoExpositor).filter(
        (
            (ConteudoExpositor.produto1_id == product_id) |
            (ConteudoExpositor.produto2_id == product_id) |
            (ConteudoExpositor.produto3_id == product_id) |
            (ConteudoExpositor.produto4_id == product_id) |
            (ConteudoExpositor.produto5_id == product_id) |
            (ConteudoExpositor.produto6_id == product_id)
        ) &
        (ConteudoExpositor.expositor_id.in_([expo.id for expo in expos]))
    ).first()

    if wantedExpo:
        session['wantedExpo'] = wantedExpo.expositor_id

    try: 
        return redirect("/Store")
    except Exception as e:
            return f'Erro ao enviar dados: {str(e)}'
    
    

@StoreClientModule.route("/SearchProduct", methods=['GET', 'POST'])
def seeSearchResult(): 
    active_user = current_user 
    form = ClienteSearchProduct()

    if(active_user.is_authenticated):
        map_id = session.get('map')
        preferedProducts = []
        searchProduct = ''
        products = '' 
 
 
        if session.get('searchingProduct') is not None:
            searchProduct = session.get('searchingProduct') 
            session.pop('searchingProduct')

        if request.method == 'POST':
            if form.searchProduct.data != None:
                searchProduct = form.searchProduct.data

        if searchProduct != '':
            productName = f"%{searchProduct}%"  # Formata o nome para corresponder parcialmente
            productName_normalized = unidecode(productName.lower())  
            

            # problema não conseguia procurar objetos com acentos
            # resolução adicionei uma coluna a tabela produtos no qual o nome é escrito com caracteres simples
            products =  db.session.query(Expositor, ConteudoExpositor, Produto).filter(
                Expositor.mapa_id == map_id, ConteudoExpositor.expositor_id == Expositor.id,
                Produto.nomeUnaccented.ilike(productName_normalized), ConteudoExpositor.produto1_id == Produto.id |
                ConteudoExpositor.produto2_id == Produto.id|ConteudoExpositor.produto3_id == Produto.id|
                ConteudoExpositor.produto4_id == Produto.id|ConteudoExpositor.produto5_id == Produto.id|
                ConteudoExpositor.produto6_id == Produto.id).all()
             

            if active_user.id != 0:
                for product in products: 
                    prefered = db.session.query(Favorito).filter(Favorito.produto_id == product[2].id, Favorito.cliente_id == active_user.id, Favorito.eliminado == 0).first()
                    if prefered:
                        preferedProducts.append(prefered)
  
            return render_template("Resultados.html", title = "MapPage", formFront = form, products = products, preferedProducts = preferedProducts, user = active_user)
        else:
            return redirect('/Store')
    else:
        return redirect("/login")
    
    # só falta realizar a procura do produto
    # depois tentar alinhar o mapa e adicionar os botões para entender se o user encontrou o produto