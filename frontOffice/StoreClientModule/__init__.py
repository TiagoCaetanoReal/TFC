from flask import Blueprint, flash, request, session
from flask import redirect, render_template, url_for
from forms import ClienteExpoDetails, ClienteLoginForm, ClienteRegisterForm, ClienteEditForm, ClienteStoreMap
from models import Iva, Medida, Origem, Produto, db, Cliente, bcrypt, Mapa, Expositor, Marcador, ConteudoExpositor, Secção
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

StoreClientModule = Blueprint("StoreClientModule", __name__)


@StoreClientModule.route("/Store", methods=['GET', 'POST'])
def seeStoreMap():
    form = ClienteStoreMap()
    active_user = current_user

    if(active_user.is_authenticated):
        if request.method == 'POST':
            print('form.expoID.data')
            print(form.expoID.data)

            if form.expoID.data != None:
                session['expo'] = form.expoID.data

                print(session)
                
                return redirect('/Displayer')

        return render_template("MapPage.html", title = "MapPage", formFront = form)
    else:
        return redirect("/login")
    


@StoreClientModule.route("/fetchMap", methods=['GET','POST'])
def fetchMap():
    print('hi')
    print('1')
    mapDictList = []
    
    # fzer queries para obter dados do mapa e mostra-lo no frontend enviando um json
    if session.get('storeID') is not None:
        map_id = session.get('storeID')

        
        map = db.session.query(Mapa).filter(Mapa.loja_id==map_id, Mapa.Usando == True).first()

        expos = db.session.query(Expositor).filter(Expositor.mapa_id == map_id, Expositor.eliminado == 0).all()
        tags = db.session.query(Marcador).filter(Marcador.mapa_id == map_id, Marcador.eliminado == 0).all()

        mapDictList.append({"width": float(map.comprimento), "height": float(map.altura), "numExpos": len(expos), "numLabels": len(tags)})

        for expo in expos:
            produtos = []
            conteudoExpositores = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.Expositor_id == expo.id, ConteudoExpositor.eliminado == 0).first()
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
    form = ClienteExpoDetails()

    if(active_user.is_authenticated):
        idExpo = session.get('expo')
        products = []

        expo = db.session.query(Expositor).filter(Expositor.id==idExpo).first()
        department = db.session.query(Secção).filter(Secção.id==expo.secção_id).first() 
        expoContent = db.session.query(ConteudoExpositor).filter(ConteudoExpositor.Expositor_id==idExpo).first()

        for index in range(expo.capacidade):
            product = db.session.query(Produto).filter(Produto.id == getattr(expoContent, f"produto{index+1}_id"), Produto.eliminado == 0).first()
            unMedida = db.session.query(Medida).filter(Medida.id == product.unMedida_id).first()
            products.append([product,unMedida])

        if request.method == 'POST':
            if form.productID.data != None:
                session['product'] = form.productID.data

        return render_template("Expositor.html", title = "ExpoPage", department = department, products = products, formFront = form )
    
    else:
        return redirect("/login")
    
    

@StoreClientModule.route("/fetchProduct", methods=['GET','POST'])
def fetchProduct():
    productDictList = []
    
    # fzer queries para obter dados do mapa e mostra-lo no frontend enviando um json
    if session.get('product') is not None:
        product_id = session.get('product')
        
        product = db.session.query(Produto).filter(Produto.id == product_id).first()
        metric = db.session.query(Medida).filter(Medida.id == product.unMedida_id).first()
        origin = db.session.query(Origem).filter(Origem.id == product.origem_id).first()
        taxes = db.session.query(Iva).filter(Iva.id == product.iva_id).first()

        nutrition100GR = db.session.query(Iva).filter(Iva.id == product.iva_id).first()
        nutritionDR = db.session.query(Iva).filter(Iva.id == product.iva_id).first()

        productDictList.append(metric.unMedida)
        productDictList.append(origin.Pais)
        productDictList.append(taxes.percentagem)

        if nutrition100GR: 
            productDictList.append(nutrition100GR)
            productDictList.append(nutritionDR)
        
  
        return productDictList
    
    else:
        return redirect('/ScanStore')