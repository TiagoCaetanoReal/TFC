import os
from flask import Blueprint, flash, request, session, send_from_directory
from flask import redirect, render_template, url_for
from forms import CreateProductForm, NutritionTableForm, ProductsListForm, EditProductForm
from models import db, Loja, Secção, Iva, Medida, Origem, Produto, TabelaNutricional100gr, TabelaNutricionalDR
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta 
from sqlalchemy.exc import SQLAlchemyError
from unidecode import unidecode

ProductsModule = Blueprint("ProductsModule", __name__)

@ProductsModule.route("/ProductsList", methods=['GET', 'POST'])
def seeProductList():
    listForm = ProductsListForm()
    active_user = current_user
    
    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
    
    if(active_user.is_authenticated): 
        departmentQuery = db.session.query(Secção).all()
        department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
        department_presets_group_list = [(' ',"Selecionar Secção")]


        for department in department_group_list:    
            department_presets_group_list.append(department)

        listForm.department.choices = department_presets_group_list

    
        storeID = active_user.loja_id
        
        produtos = db.session.query(Produto, Secção).filter(Produto.loja_id == storeID, Produto.secção_id == Secção.id, Produto.eliminado == False).all()

        if produtos:
            if request.method == 'POST':
                acao = listForm.action.data

                if(acao == 'Editar'):
                    idproduto = listForm.productId.data
                    session['produto'] = idproduto

                    return redirect('/EditProduct')
                
                elif(acao == 'DeleteProducts'):
                    productsToDelete = listForm.productsToDelet.data.split(",") 
                    nested_transaction = db.session.begin_nested()

                    for productToDelete in productsToDelete: 
                        product = db.session.query(Produto).filter(Produto.id == productToDelete).first()
                        product.eliminado = True

                    nested_transaction.commit()
                    db.session.commit()

                    return redirect('/ProductsList')



    else:
        return redirect("/login")
    
    return render_template("ListagemProdutos.html", title = "MapList", active_user = employee, produtos = produtos, listFormFront = listForm)
  

@ProductsModule.route("/MakeProduct", methods=['GET', 'POST'])
def CreateProduct():
    productForm = CreateProductForm()
    nutritionForm = NutritionTableForm()

    active_user = current_user

    if(active_user.is_authenticated):
        departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
        employee = [active_user.nome,active_user.cargo,departemant.nome]

        store = db.session.query(Loja).filter(Loja.id==active_user.loja_id).first()

        #query para o iva 
        ivaQuery = db.session.query(Iva).all()
        iva_group_list=[(str(i.id), str(i.percentagem)+'%') for i in ivaQuery]
        iva_presets_group_list = [(' ',"Selecionar Iva")]

        for iva in iva_group_list:    
            iva_presets_group_list.append(iva)

        productForm.iva.choices = iva_presets_group_list


        #query para a unidade de medida
        metricQuery = db.session.query(Medida).all()
        metric_group_list=[(str(i.id), i.unMedida) for i in metricQuery]
        metric_presets_group_list = [(' ',"Selecionar Unidade de Medida")]

        for metric in metric_group_list:    
            metric_presets_group_list.append(metric)

        productForm.metric.choices = metric_presets_group_list


        #query para a origem 
        originQuery = db.session.query(Origem).all()
        origin_group_list=[(str(i.id), i.Pais) for i in originQuery]
        origin_presets_group_list = [(' ',"Selecionar Origem")]

        for origin in origin_group_list:    
            origin_presets_group_list.append(origin)

        productForm.origin.choices = origin_presets_group_list


        #query para a secção
        departmentQuery = db.session.query(Secção).all()
        department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
        department_presets_group_list = [(' ',"Selecionar Secção")]
    
    
        for department in department_group_list:    
            department_presets_group_list.append(department)

        productForm.department.choices = department_presets_group_list


        if request.method == 'POST':
            if productForm.validate() and productForm.createProduct.data == True:
                produto = db.session.query(Produto).filter(Produto.loja_id == store.id, Produto.nome == productForm.name.data).first()

                if(produto == None):
                    seccao = dict(productForm.department.choices).get(productForm.department.data)

                    saveImgDir = './static/productPhotos/'+str(store.id)+'/'+ str(seccao).replace(' ', '_')+'/'
  
                    if not os.path.exists(saveImgDir):
                        os.makedirs(saveImgDir)

                    destination = os.path.join(saveImgDir, productForm.name.data.replace(' ', '_') + 'Image.png')
                    
                    request.files['photoFile'].save(destination)

                    # caso o primeiro elemento do valor seja . por exemplo .99 é adicionado 0 ao inicio para ficar 0.99
                    if str(productForm.price.data)[0] == '.':
                        productForm.price.data = float(str(0) + str(productForm.price.data))

                    try:
                        new_Product = Produto(nome=productForm.name.data, nomeUnaccented = unidecode(productForm.name.data).lower(), preço = productForm.price.data, 
                                            origem_id = productForm.origin.data, iva_id = productForm.iva.data, 
                                            unMedida_id = productForm.metric.data, secção_id = productForm.department.data, 
                                            photoPath = destination, loja_id = store.id)
                        
                        db.session.add(new_Product)

                        fullyFilled, partFilled = isFormFilled(nutritionForm)

                        if(fullyFilled and not partFilled):
                            db.session.commit()
                            get_produto = db.session.query(Produto).filter(Produto.loja_id == store.id, Produto.nome == productForm.name.data).first()


                            new_100grTable =  TabelaNutricional100gr(
                                kcal = nutritionForm.kcal100gr.data, kj = nutritionForm.kj100gr.data,
                                lipidos = nutritionForm.lipids100gr.data, hidratos = nutritionForm.carbohydrates100gr.data,
                                fibras = nutritionForm.sugars100gr.data, proteinas = nutritionForm.fibers100gr.data, 
                                açúcares = nutritionForm.protein100gr.data,sal = nutritionForm.salt100gr.data, produto_id = get_produto.id)
                        
                            new_DRTable = TabelaNutricionalDR(
                                kcal = nutritionForm.kcalDR.data, kj = nutritionForm.kjDR.data,
                                lipidos = nutritionForm.lipidsDR.data, hidratos = nutritionForm.carbohydratesDR.data,
                                fibras = nutritionForm.sugarsDR.data, proteinas = nutritionForm.fibersDR.data, 
                                açúcares = nutritionForm.proteinDR.data,sal = nutritionForm.saltDR.data, produto_id = get_produto.id)

                            db.session.add(new_100grTable)
                            db.session.add(new_DRTable)
                            db.session.commit()
                            
                            return redirect('/ProductsList')
                    
                        elif(not fullyFilled and partFilled):
                            l = list(nutritionForm.kcal100gr.errors)
                            l.append("Ao preencher uma celula da tabela tem de a preencher toda")
                            nutritionForm.kcal100gr.errors = tuple(l)

                        elif(not fullyFilled and not partFilled):
                            db.session.commit()
                            return redirect('/ProductsList')

                    except Exception as e:
                        return f'Erro ao salvar o produto: {str(e)}'
            
                else :
                    l = list(productForm.name.errors)
                    l.append("Este nome de produto já existe na loja")
                    productForm.name.errors = tuple(l)


        return render_template("CriarProduto.html", title = "MakeProduct", active_user = employee, productFormFront = productForm, nutritionFormFront = nutritionForm)

    else:
        return redirect("/login")


# verificar se há campos por preencher na tabela
def isFormFilled(form):
    form_data = form._fields
    counter = len(form_data) -1

    for field in form_data:
        if form[field].data :
            counter -= 1
    
    counter += 1
    
    if (counter < len(form_data)-1 and counter > 0):
        return False, True
    
    elif (counter == len(form_data) -1):
        return False, False
    else:
        return True, False

 
@ProductsModule.route("/EditProduct", methods=['GET','POST'])
def AlterProduct():
    productForm = EditProductForm()
    nutritionForm = NutritionTableForm()

    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]


    if(active_user.is_authenticated): 
        ivaQuery = db.session.query(Iva).all()
        iva_group_list=[(str(i.id), str(i.percentagem)+'%') for i in ivaQuery]
        iva_presets_group_list = [(' ',"Selecionar Iva")]

        for iva in iva_group_list:    
            iva_presets_group_list.append(iva)

        productForm.iva.choices = iva_presets_group_list

 
        metricQuery = db.session.query(Medida).all()
        metric_group_list=[(str(i.id), i.unMedida) for i in metricQuery]
        metric_presets_group_list = [(' ',"Selecionar Unidade de Medida")]

        for metric in metric_group_list:    
            metric_presets_group_list.append(metric)

        productForm.metric.choices = metric_presets_group_list

 
        originQuery = db.session.query(Origem).all()
        origin_group_list=[(str(i.id), i.Pais) for i in originQuery]
        origin_presets_group_list = [(' ',"Selecionar Origem")]

        for origin in origin_group_list:    
            origin_presets_group_list.append(origin)

        productForm.origin.choices = origin_presets_group_list

 
        departmentQuery = db.session.query(Secção).all()
        department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
        department_presets_group_list = [(' ',"Selecionar Secção")]
 

        for department in department_group_list:    
            department_presets_group_list.append(department)

        productForm.department.choices = department_presets_group_list

        if session.get('produto') is not None:
            product_id = session.get('produto')
            produto = db.session.query(Produto).filter(Produto.id==product_id).first()

            tabela100gr = db.session.query(TabelaNutricional100gr).filter(TabelaNutricional100gr.produto_id==product_id).first()
            tabelaDR = db.session.query(TabelaNutricionalDR).filter(TabelaNutricionalDR.produto_id==product_id).first()
 
            if request.method == 'POST':
                listProduct  = ['nome', 'preço', 'iva_id','unMedida_id','origem_id', 'secção_id', 'photoPath']
                nutritionalList = ['kcal', 'kj', 'lipidos', 'hidratos', 'açúcares','fibras', 'proteinas', 'sal']
 
                if productForm.validate() and productForm.editProduct.data == True:
                    try:
                        for index, field in enumerate(productForm):
                            if index < 7:
                                valor = listProduct[index]
                                
                                if str(field.data) != str(getattr(produto, valor)) and str(field.data) != '':
                                    if(valor == 'nome'):
                                        nomeUnaccented = unidecode(field.data).lower()
                                        setattr(produto, 'nomeUnaccented', nomeUnaccented)
 

                                    if(valor == 'photoPath'):
                                        field.data = save_photo(produto)

                                    setattr(produto, valor, field.data)



                        fullyFilled, partFilled = isFormFilled(nutritionForm)

                        print(fullyFilled)
                        print(partFilled)

                               
                        if(fullyFilled and not partFilled):
                            for index, field in enumerate(nutritionForm):
                                if tabela100gr and tabelaDR:  
                                    if index < 8 :   
                                        valorNutritionalList = nutritionalList[index]
                                        
                                        if str(field.data) != str(getattr(tabela100gr, valorNutritionalList)) and str(field.data) != '':
                                            setattr(tabela100gr, valorNutritionalList, field.data)
                                        
                                    if index >= 8 and index < 16:    
                                        valorNutritionalList = nutritionalList[index-8]
                                        if str(field.data) != str(getattr(tabelaDR, valorNutritionalList)) and str(field.data) != '':
                                            setattr(tabelaDR, valorNutritionalList, field.data)
                                
                                else:  
                                    new_100grTable =  TabelaNutricional100gr(
                                        kcal = nutritionForm.kcal100gr.data, kj = nutritionForm.kj100gr.data,
                                        lipidos = nutritionForm.lipids100gr.data, hidratos = nutritionForm.carbohydrates100gr.data,
                                        fibras = nutritionForm.sugars100gr.data, proteinas = nutritionForm.fibers100gr.data, 
                                        açúcares = nutritionForm.protein100gr.data,sal = nutritionForm.salt100gr.data, produto_id = product_id)
                                
                                    new_DRTable = TabelaNutricionalDR(
                                        kcal = nutritionForm.kcalDR.data, kj = nutritionForm.kjDR.data,
                                        lipidos = nutritionForm.lipidsDR.data, hidratos = nutritionForm.carbohydratesDR.data,
                                        fibras = nutritionForm.sugarsDR.data, proteinas = nutritionForm.fibersDR.data, 
                                        açúcares = nutritionForm.proteinDR.data,sal = nutritionForm.saltDR.data, produto_id = product_id)

                                    db.session.add(new_100grTable)
                                    db.session.add(new_DRTable) 
                                    
                            db.session.commit()
                            return redirect('/ProductsList')

                        elif(not fullyFilled and partFilled):
                            l = list(nutritionForm.kcal100gr.errors)
                            l.append("Ao preencher uma celula da tabela tem de a preencher toda")
                            nutritionForm.kcal100gr.errors = tuple(l)

                        elif(not fullyFilled and not partFilled):
                            db.session.commit()
                            return redirect('/ProductsList')
                         
                    
                    except SQLAlchemyError as e:
                        print(f'Erro ao editar o produto: {str(e)}')
            
        return render_template('EditarProduto.html', title="EditProduct", active_user=employee, produtoFront = produto, tabela100grFront = tabela100gr, 
            tabelaDRFront = tabelaDR, productFormFront = productForm, nutritionFormFront=nutritionForm)
        
    else:
        return redirect('/login')
    
   
# alterar o sitio onde é guardada foto, e alterar o nome da foto segundo: 
def save_photo(produto):
    departemant = db.session.query(Secção).filter(Secção.id==produto.secção_id).first()

    saveImgDir = './static/productPhotos/'+str(produto.loja_id)+'/'+ str(departemant.nome).replace(' ', '_')+'/'

    if not os.path.exists(saveImgDir):
        os.makedirs(saveImgDir)

    photoPath = os.path.join(saveImgDir, produto.nome.replace(' ', '_') + 'Image.png') 

    request.files['photoFile'].save(photoPath)
    return photoPath