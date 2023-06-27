import os
from flask import Blueprint, flash, request, session, send_from_directory
from flask import redirect, render_template, url_for
from forms import CreateProductForm, NutritionTableForm, ProductsListForm, EditProductForm
from models import db, Loja, Secção, Iva, Medida, Origem, Produto, TabelaNutricional100gr, TabelaNutricionalDR
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import shutil

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
        storeID = active_user.loja_id
        
        produtos = db.session.query(Produto, Secção).filter(Produto.loja_id == storeID, Produto.secção_id == Secção.id).all()


        if request.method == 'POST':
            idproduto = listForm.productId.data
            session['produto'] = idproduto
            print(idproduto)

            return redirect('/EditProduct')


    else:
        return redirect("/login")
    
    print("list")
    
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

                print(nutritionForm.kcal100gr.errors)


        return render_template("CriarProduto.html", title = "MakeProduct", active_user = employee, productFormFront = productForm, nutritionFormFront = nutritionForm)

    else:
        return redirect("/login")
    

# verificar se há campos por preencher
def isFormFilled(form):
    form_data = form._fields
    counter = len(form_data) -1
    
    print(counter)

    for field in form_data:
        if form[field].data :
            counter -= 1
    
    counter += 1
    
    if (counter < len(form_data)-1 and counter > 0):
        
        print(counter <= len(form_data)-1)
        print(counter <= len(form_data))
        print(counter)
        return False, True
    
    elif (counter == len(form_data) -1):
        print(counter)
        return False, False
    else:
        print(counter)
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

    if session.get('produto', None) is not None:
        product_id = session.get('produto')
        produto = db.session.query(Produto).filter(Produto.id==product_id).first()

        tabela100gr = db.session.query(TabelaNutricional100gr).filter(TabelaNutricional100gr.produto_id==product_id).first()
        tabelaDR = db.session.query(TabelaNutricionalDR).filter(TabelaNutricionalDR.produto_id==product_id).first()

        # pathPhoto = load_file(produto.photoPath)

        print(produto.photoPath)

        # tentar realizar a procura de campos preenchidos de forma dinamica e ao fazer-lo inserir nos dado da query para fazer o update 
        #  provavelmente terei de ter os nomes iguais dos dois lados, ou... ou ...
        #  posso fazer um dicionario com as posiçoes dos campos do modelo ou do form
       
    # tentado o debaixo para fazer um dict com as posicçoes dos campos do modelo para 
    # fazer um ciclo pelos campos do form e caso esse campo tenha sido preenchido 
    # verifica com o dict o atributo do modelo e troca o seu valor
    # tipo dict('nome': 1, 'preço':2) -> ('atributo modelo': posição no form)
#        produto = db.session.query(Produto).filter(Produto.id == product_id).first()

# if produto:
#     atributos = vars(produto)
    
#     for indice in atributos:
#         atributo = atributos[indice]
#         valor = getattr(produto, atributo)
#         print(f'{atributo}: {valor}')
# else:
#     print("Produto não encontrado.")
       
       
        atributos = vars(produto)
        for atributo, valor in atributos.items():
            print(f'{atributo}: {valor}')

        for field in productForm:
            if field.data:
                print(field.name)
            else:
                print("nothing " + field.name)
        
        
        return render_template('EditarProduto.html', title="EditProduct", active_user=employee, produtoFront = produto, tabela100grFront = tabela100gr, 
                               tabelaDRFront = tabelaDR, productFormFront = productForm, nutritionFormFront=nutritionForm)
    
    
    return render_template('EditarProduto.html', title="EditProduct", active_user=employee, produtoFront = produto, productFormFront = productForm, nutritionFormFront=nutritionForm)
 
# def load_file(filename):
#     return send_from_directory('', filename)
