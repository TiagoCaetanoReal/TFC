import os
from flask import Blueprint, flash, request, session, send_from_directory
from flask import redirect, render_template, url_for
from forms import CreateProductForm, NutritionTableForm, ProductsListForm, EditProductForm
from models import db, Loja, Secção, Iva, Medida, Origem, Produto, TabelaNutricional100gr, TabelaNutricionalDR
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import shutil
from sqlalchemy.exc import SQLAlchemyError

ProductsModule = Blueprint("ProductsModule", __name__)

# problema ao clicar no botão editar, no qual consigo receber o id do produto, porem
# não consigo mudar o template
# tentar usar um form para ir buscar o id
@ProductsModule.route("/ProductsList", methods=['GET', 'POST'])
def seeProductList():
    listForm = ProductsListForm()
    active_user = current_user
    
    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
    
    if(active_user.is_authenticated):
        #query para a secção
        departmentQuery = db.session.query(Secção).all()
        department_group_list=[(str(i.id), i.nome) for i in departmentQuery]
        department_presets_group_list = [(' ',"Selecionar Secção")]


        for department in department_group_list:    
            department_presets_group_list.append(department)

        listForm.department.choices = department_presets_group_list

    
        storeID = active_user.loja_id
        
        produtos = db.session.query(Produto, Secção).filter(Produto.loja_id == storeID, Produto.secção_id == Secção.id).all()

        if produtos:
            if request.method == 'POST':
                idproduto = listForm.productId.data
                session['produto'] = idproduto

                return redirect('/EditProduct')


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

                    saveImgDir = './static/productPhotos/'+str(store.id)+'/'+ str(seccao)+'/'

                    # alterar o sitio onde é guardada foto, e alterar o nome da foto segundo:
                    # https://www.youtube.com/watch?v=ZHQtxITPcAs&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=38
                
                    
                    if not os.path.exists(saveImgDir):
                        os.makedirs(saveImgDir)


                    destination = os.path.join(saveImgDir, productForm.name.data + 'Image.png')
                    

                    request.files['photoFile'].save(destination)

                    try:
                        new_Product = Produto(nome=productForm.name.data, preço = productForm.price.data, 
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


# verificar se há campos por preencher
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



# problema ao clicar no botão editar, no qual consigo receber o id do produto, porem
# não consigo mudar o template
# tentar passar o id do produto de forma escondida
# resolução no script do js, adicionei o submit para enviar o form
@ProductsModule.route("/EditProduct", methods=['GET','POST'])
def AlterProduct():
    productForm = EditProductForm()
    nutritionForm = NutritionTableForm()

    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]


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

    if session.get('produto') is not None:
        product_id = session.get('produto')
        produto = db.session.query(Produto).filter(Produto.id==product_id).first()

        tabela100gr = db.session.query(TabelaNutricional100gr).filter(TabelaNutricional100gr.produto_id==product_id).first()
        tabelaDR = db.session.query(TabelaNutricionalDR).filter(TabelaNutricionalDR.produto_id==product_id).first()


        # tentar realizar a procura de campos preenchidos de forma dinamica e ao fazer-lo inserir no dado da query para fazer o update 
        #  provavelmente terei de ter os nomes iguais dos dois lados, ou... ou ...
        #  posso fazer um dicionario com as posiçoes dos campos do modelo ou do form
       
        # tentado o debaixo para fazer um dict com as posicçoes dos campos do modelo para 
        # fazer um ciclo pelos campos do form e caso esse campo tenha sido preenchido 
        # verifica com o dict o atributo do modelo e troca o seu valor
        # tipo dict('nome': 1, 'preço':2) -> ('atributo modelo': posição no form)

        if request.method == 'POST':
            listProduct  = ['nome', 'preço', 'iva_id','unMedida_id','origem_id', 'secção_id', 'photoPath']

            # tentar adicionar o modal na parte da frente
            
            if productForm.validate() and productForm.editProduct.data == True:
                try:
                    for index, field in enumerate(productForm):
                        if index < 7:
                            valor = listProduct[index]
                            
                            if str(field.data) != str(getattr(produto, valor)) and str(field.data) != '':
                                # if(valor == 'nome'):
                                #     novo_nome = "Image.png"

                                #     print(produto.photoPath)

                                #     # guarda imagem mas não subscreve, depois disso é só fazer as tabela e a edição fica pronta

                                #     productForm.photoURI.data = os.rename(produto.photoPath, field.data + novo_nome)

                                #     print(productForm.photoURI.data)

                                if(valor == 'photoPath'):
                                    field.data = save_photo(produto)
                                    print(field.data)
                                setattr(produto, valor, field.data)

                    # problema commit não esta a funcionar
                    # solução  remover atributos[valor] e utilizar  setattr(produto, valor, field.data) 
                    # para armazenar o valor modificado objeto da db
                    db.session.commit()

                    return redirect('/ProductsList')
                except SQLAlchemyError as e:
                    print(f'Erro ao editar o produto: {str(e)}')
                finally:
                    print("Após o commit")
                    print("Objeto modificado:", produto.nome)
                    
                    
        
        return render_template('EditarProduto.html', title="EditProduct", active_user=employee, produtoFront = produto, tabela100grFront = tabela100gr, 
                               tabelaDRFront = tabelaDR, productFormFront = productForm, nutritionFormFront=nutritionForm)
    
    
 

# alterar o sitio onde é guardada foto, e alterar o nome da foto segundo:
# https://www.youtube.com/watch?v=ZHQtxITPcAs&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=38
def save_photo(produto):
    departemant = db.session.query(Secção).filter(Secção.id==produto.secção_id).first()

    saveImgDir = './static/productPhotos/'+str(produto.loja_id)+'/'+ str(departemant.nome)+'/'

    if not os.path.exists(saveImgDir):
        os.makedirs(saveImgDir)

    photoPath = os.path.join(saveImgDir, produto.nome + 'Image.png')
    print(photoPath)

    request.files['photoFile'].save(photoPath)
    return photoPath