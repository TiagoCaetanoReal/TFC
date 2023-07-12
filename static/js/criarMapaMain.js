import { Expositor } from './expositor.js';
import { TextBlock } from './textblock.js';
import { Quadro } from './quadro.js';
import * as tools from './ferramentasQuadro.js';

// elementos html
var addExpo = document.getElementById("addExpositor")
var rotateExpo = document.getElementById("rotateExpositor")
var excludeExpo = document.getElementById("excludeExpositor")
var resizeExpo = document.getElementById("resizeExpositor")
var detailExpo = document.getElementById("detailExpositor")
var capacity = document.getElementById("selectCapacity")
var departmants = document.getElementById("selectSector")
var divisions = document.getElementById("selectDivision")
var produtos = document.getElementById("addProdutos")
var texts = document.getElementById("addText")
var createMap = document.getElementById("CreateMap")
var deleteMap = document.getElementById("DeleteMap")
var discardExpoInfo = document.getElementById("discardExpoInfo")
var saveExpoInfo = document.getElementById("saveExpoInfo")
var mapFormField = document.getElementById("mapa")

let selectedExpositor;


// https://www.youtube.com/watch?v=7PYvx8u_9Sk

var myModal = new bootstrap.Modal(document.getElementById('instructionsModal'), {})
myModal.toggle()

let canvas = new Quadro(document.getElementById("canvas"), document.getElementById("canvas").getContext("2d"));
canvas.detectAction();
let sizeX = canvas.canvas_width;
let sizeY = canvas.canvas_height;

addExpo.onmousedown = (event) =>{
    canvas.addExpositores(new Expositor(canvas.shapes.length,sizeX/2,sizeY/2, 20, 60, 'grey'));
}

rotateExpo.onmousedown = (event) =>{
    try {
        if(canvas.selectedExpo){  
            canvas.getShapes()[canvas.getCurrentExpositorIndex()].rotate_expositor(); 
        }
        else if(canvas.selectedText){ 
            // tentando mudar a seleção do texto, para que quando este roda, a seleção do rato se adapte à rotação ln-120 de quadro.js
            var text = canvas.getTexts()[canvas.getSelected(canvas.getTexts())];
            canvas.rotateText(text)
        }
        else
            throw new TypeError('');

        canvas.resizeShapes = [];
        
    } catch (error) {
        window.alert("Selecione um expositor/texto para realizar esta ação");
    }
    
    canvas.draw_shapes();
}

excludeExpo.onmousedown = (event) =>{ 
    try {
        if(canvas.selectedExpo){
            const alteredShapes = tools.excludeExpositores(canvas.getShapes(), canvas.getSelected(canvas.getShapes()));
            canvas.setShapes(alteredShapes);
            canvas.resizeShapes = [];
        }
        else if(canvas.selectedText){
            const alteredTexts = tools.excludeText(canvas.getTexts(),canvas.getSelected(canvas.getTexts()));
            canvas.setTexts(alteredTexts);
        }
    
        else
            throw new TypeError('');

    } catch (error) {
        console.log(error);
        window.alert("Selecione um expositor para realizar esta ação"); 
    }
    
    canvas.draw_shapes();
}

resizeExpo.onmousedown = (event) =>{
    try {
        if(canvas.selectedExpo){
            let selectedExpositor = canvas.getSelected(canvas.getShapes())
            
            const [shape, resizers] = tools.resizers(canvas.getShapes(),  canvas.getResizeShapes(), selectedExpositor)

            canvas.setSelectedShape(shape)
            canvas.setResizeShapes(resizers)
            
            // canvas.resizers(selectedExpositor)
        }
        else
            throw new TypeError('');

    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação"); 
    }
    
    canvas.draw_shapes();
}

detailExpo.onmousedown = (event) =>{
    produtos.innerHTML = '';
    
    try {
        if(canvas.selectedExpo){
            selectedExpositor = canvas.getCurrentExpositor();

            capacity.onchange = (event) => {
                var inputText = event.target.value;
                
                selectedExpositor.capacity = parseInt(inputText);
        
        
                createProductSpaces(inputText);
        
                // tou a ter problemas de que os campos ficam salvos do expo anterio no novo
                
                // modifica comment abaixo, vou fazer o seguinte, fazer fetch dos produtos, quando se tiver a capacidade e a secção, 
                // caso contrario não chama o metodo acho createProductSpaces
                //nesta parte após serem criados os selects dos produtos, tem de ser mandado do backend um array ou string com os produtos, possivelmente um array
            }
        
            
            departmants.onchange = (event) => {
                // https://www.youtube.com/watch?v=exRAM1ZWm_s
                var inputText = event.target.value;
                selectedExpositor.storeSection = parseInt(inputText);
        
                fetch("/fetchColor?seccaoId=" + inputText)
                .then(response => response.json())
                .then(data => {
                    var cor = data.cor;
        
                    selectedExpositor.give_colorSection(cor);
                });
        
                createProductSpaces(capacity.value);
            }
            
            divisions.onchange = (event) => {
                var inputText = event.target.value;
                selectedExpositor.divisions = parseInt(inputText);
            }
        
            produtos.onchange = (event) => {
                var inputSpaceNumber = event.target.id.charAt(event.target.id.length - 1)
        
                if( selectedExpositor.products[inputSpaceNumber] !== ' '){
                    selectedExpositor.products[inputSpaceNumber] = event.target.value;
                }else{
                    selectedExpositor.products.push(event.target.value) ;
                }
            }
                        
            if(selectedExpositor.capacity === 0){
                capacity.value = selectedExpositor.capacity;
                selectedExpositor.products = [];
                
            }else{
                capacity.value = selectedExpositor.capacity;
                createProductSpaces(capacity.value);
            }
        
            if(selectedExpositor.storeSection === 0){
                departmants.value = ' ';
            }else{
                departmants.value =  selectedExpositor.storeSection.toString(); 
            }
            if(selectedExpositor.divisions === 0){
                divisions.value = "0";
            }else{
                divisions.value =  selectedExpositor.divisions.toString();
            }
        }
        else
            throw new TypeError('');
    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação");
    }  


    const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    const myModalTitle = new bootstrap.Modal(document.getElementById('staticBackdropLabel'));

    myModalTitle._element.innerText = 'Expositor ' + selectedExpositor.id;


    function createProductSpaces(numProducts) {
        const node = ''

        if(capacity.value !== '0' && departmants.value !== ' '){
            fetch("/fetchProducts?seccaoId=" + selectedExpositor.storeSection)
            .then(response => response.json())
            .then(data => {
                var products = data.products;


                produtos.innerHTML = '';
                    
                for(let i = 0; i<numProducts; i++ ){
                    const node = `
                        <div class="col-6">
                            <div class="input-group my-1 needs-validation py-2">
                                <select id="selectProduct${i}" class="form-select" required> 
                                    <option class="is-invalid" disabled selected value=' '>Selecionar Produto</option>
                                </select><div class="invalid-feedback">Por Favor selecione um produto</div> 
                            </div>
                        </div>
                    `; 

                    produtos.innerHTML += node
                }

                var numChilds =  produtos.childElementCount;


                for (let index = 0; index < numChilds; index++) {
                    var selector = document.getElementById("selectProduct"+index);

                    products.forEach(element => {
                        console.log(element.id);
                        console.log(element.nome);
                        let newOption = new Option(element.nome, element.id);

                        selector.add(newOption,undefined);
                    });
                }

                var numChildsAssigned = selectedExpositor.products.length;

                if(numChildsAssigned > 0){
                    for(let i = 0; i<numChildsAssigned; i++ ){
                        document.getElementById("selectProduct"+i).value = [selectedExpositor.products[i]]
                    }
                        
                }  
                
                else{
                    for(let i = 0; i<numChildsAssigned; i++ ){
                        document.getElementById("selectProduct"+i).value = 0
                    }
            
                }              
                
            });
        }
    }
    
    myModal.toggle();
    myModal.show();

    discardExpoInfo.onclick = (event) =>{ 
        produtos.innerHTML = '';
        selectedExpositor.products = [];
        selectedExpositor.capacity = 0;
        selectedExpositor.divisions = 0;
        selectedExpositor.storeSection = 0;
        selectedExpositor.storeSectionColor = '';

    }


}




texts.onmousedown = (event) =>{
    const myModal = new bootstrap.Modal(document.getElementById('addTextBackdrop'));
    const addTextBtn = document.getElementById('addTextBtn')
    const textInput = document.getElementById('textInput')
    
    addTextBtn.onclick = (event) =>{
        canvas.addTextBlock(new TextBlock(canvas.texts.length,sizeX/2,sizeY/2,textInput.value, 0));
        textInput.value = '';
    }

    CancelTextBtn.onclick = (event) =>{
        textInput.value = '';
    }

    myModal.toggle();
    myModal.show();
}



createMap.onmousedown = (event) =>{
    let array = []
    let index = 0

    const myModal = new bootstrap.Modal(document.getElementById('saveDeleteMap'));
    const myModalTitle = new bootstrap.Modal(document.getElementById('saveDeleteMapTitle'));

    myModalTitle._element.innerText = "Deseja guardar o mapa criado?"

    myModal.toggle();
    myModal.show();

    
    const elemento = document.getElementById('discardBtn');
    elemento.setAttribute('hidden', 'true');

    ConfirmSaveDeleteBtn.removeAttribute('hidden');

    ConfirmSaveDeleteBtn.onclick = (event) =>{
        array[index] = {"width": sizeX,"height": sizeY, "numExpos": canvas.getShapes().length, "numLabels": canvas.getTexts().length};
        index ++;

        console.log(canvas.getShapes());
        
        canvas.getShapes().forEach(element => {
            array[index] = {"id": element.id, "posX": element.posX, "posY": element.posY, "width": element.width,
                            "height": element.height, "products": element.products, "capacity": element.capacity, 
                            "divisions": element.divisions, "storeSection": element.storeSection};
            index ++;
        });

        canvas.getTexts().forEach(element => {
            array[index] = {"id": element.id, "posX": element.posX, "posY": element.posY, "width": element.width,
                            "height": element.height, "angle": element.angle, "value": element.text};
            index ++;
        });

        let json = JSON.stringify(array)

        mapFormField.value = json

        console.log(mapFormField);
        
        // Envie o formulário
        
        document.getElementById("formulario").submit()
    }
}

deleteMap.onmousedown = (event) =>{
        const myModal = new bootstrap.Modal(document.getElementById('saveDeleteMap'));
        const myModalTitle = new bootstrap.Modal(document.getElementById('saveDeleteMapTitle'));
    
        myModalTitle._element.innerText = "Deseja descartar o mapa criado?"
    
        myModal.toggle();
        myModal.show();

        
        const elemento = document.getElementById('discardBtn');
        elemento.removeAttribute('hidden');

        ConfirmSaveDeleteBtn.setAttribute('hidden', 'true');
    }







//https://stackoverflow.com/questions/22785521/how-can-i-drag-a-piece-of-user-generated-text-around-the-html5-canvas

