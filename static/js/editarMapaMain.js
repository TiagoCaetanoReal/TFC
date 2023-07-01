import { Expositor } from './expositor.js';
import { TextBlock } from './textblock.js';
import { Quadro } from './quadro.js';

// https://www.youtube.com/watch?v=7PYvx8u_9Sk



// modal das instruções esta desativado \|/
// var myModal = new bootstrap.Modal(document.getElementById('instructionsModal'), {})
// myModal.toggle()

let canvas = new Quadro(document.getElementById("canvas"), document.getElementById("canvas").getContext("2d"));
canvas.detectAction();
let sizeX = canvas.canvas_width;
let sizeY = canvas.canvas_height;

let array = [];
array = JSON.parse(localStorage.getItem("map") || "[]");

const numExpos = array[0].numExpos;

let index = 0


array.shift();

array.forEach(element => {
    if(index < numExpos){
        console.log(element);
        if(element.storeSection === 0){
            canvas.addExpositores(new Expositor(element.id, element.posX , element.posY , element.width, element.height, element.color.toString()));
            console.log(canvas.getShapes());
        }
        else{
            canvas.addExpositores(new Expositor(element.id, element.posX, element.posY,  element.width, element.height, element.color.toString(), 
                element.products, element.capacity, element.divisions, element.storeSection, element.storeSectionColor.toString())); 
                
            console.log(canvas.getShapes());
        }
    }
   else{
        canvas.addTextBlock(new TextBlock(element.id, element.posX, element.posY, element.value, element.angle));
   }
   index++;
});


// Adiciona o listener de resize à janela do navegador
// window.addEventListener("resize", canvas.resizeCanvas, false);


document.getElementById("addExpositor").onmousedown = (event) =>{
    canvas.addExpositores(new Expositor(canvas.shapes.length,sizeX/2,sizeY/2, 20, 60, 'grey'));
}

document.getElementById("rotateExpositor").onmousedown = (event) =>{
    try {
        if(canvas.selectedExpo){
            canvas.getShapes()[canvas.getSelected(canvas.getShapes())].rotate_expositor();
        }
        else if(canvas.selectedText){
            
            // tentando mudar a seleção do texto, para que quando este rode, a seleção do rato se adapte à rotação ln-120 de quadro.js
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

document.getElementById("excludeExpositor").onmousedown = (event) =>{ 
    try {
        if(canvas.selectedExpo){
            canvas.excludeExpositores(canvas.getSelected(canvas.getShapes()))
            canvas.resizeShapes = [];
        }
        else if(canvas.selectedText){
            // var text = canvas.getTexts()[canvas.getSelected(canvas.getTexts())];
            canvas.excludeText(canvas.getSelected(canvas.getTexts()))
            
        }
    
        else
            throw new TypeError('');

    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação"); 
    }
    
    canvas.draw_shapes();
}

document.getElementById("resizeExpositor").onmousedown = (event) =>{
    try {
        if(canvas.selectedExpo){
            let selectedExpositor = canvas.getSelected(canvas.getShapes())
            canvas.resizers(selectedExpositor)
        }
        else
            throw new TypeError('');

    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação"); 
    }
    
    canvas.draw_shapes();
}

document.getElementById("detailExpositor").onmousedown = (event) =>{
    let selectedExpositor;
    try {
        if(canvas.selectedExpo){
            selectedExpositor = canvas.getCurrentExpositor();

            let capacity = document.getElementById('selectCapacity')

            console.log(selectedExpositor.capacity)
            console.log(capacity)

            // resolver problema de caso expo não tenha produtos, da segunda vez q se entra nele, os campos estão vazios

            console.log(selectedExpositor.capacity === 0)

            if(selectedExpositor.capacity === 0){
                console.log("1")
                capacity.value = selectedExpositor.capacity;
                document.getElementById("addProdutos").innerHTML = '';
                selectedExpositor.products = [];
                
            }else{
                console.log("2")
                capacity.value = selectedExpositor.capacity;

                createProductSpaces(capacity.value);


                for (let index = 0; index < parseInt(capacity.value); index++) {
                    var productSpace = document.getElementById('selectProduct'+index);

                    var ExpositorProduct = selectedExpositor.products[index];
                    console.log(ExpositorProduct)
                    if(ExpositorProduct !== undefined)
                        productSpace.value = ExpositorProduct.toString();
                }
            }
        
            if(selectedExpositor.storeSection === 0){
                document.getElementById('selectSector').value = "0";
            }else{
                document.getElementById('selectSector').value =  selectedExpositor.storeSection.toString(); 
            }
        
            if(selectedExpositor.divisions === 0){
                document.getElementById('selectDivision').value = "0";
            }else{
                document.getElementById('selectDivision').value =  selectedExpositor.divisions.toString();
            }
        }
        else
            throw new TypeError('');
    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação");
        console.log('6')
    }  

    
    const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    const myModalTitle = new bootstrap.Modal(document.getElementById('staticBackdropLabel'));

    myModalTitle._element.innerText = 'Expositor ' + selectedExpositor.id;



    document.getElementById('selectCapacity').onchange = (event) => {
        var inputText = event.target.value;
        selectedExpositor.capacity = parseInt(inputText);

        createProductSpaces(inputText);
 

        //nesta parte após serem criados os selects dos produtos, tem de ser mandado do backend um array ou string com os produtos, possivelmente um array
    }

    
    document.getElementById('selectSector').onchange = (event) => {
        var inputText = event.target.value;
        selectedExpositor.storeSection = parseInt(inputText);
        selectedExpositor.give_colorSection('blue');
    }
    
    document.getElementById('selectDivision').onchange = (event) => {
        var inputText = event.target.value;
        selectedExpositor.divisions = parseInt(inputText);
    }

    document.getElementById("addProdutos").onchange = (event) => {
        var inputSpaceNumber = event.target.id.charAt(event.target.id.length - 1)

        if( selectedExpositor.products[inputSpaceNumber] != ''){
            selectedExpositor.products[inputSpaceNumber] = event.target.value;
        }else{
            selectedExpositor.products.push(event.target.value) ;
        }
    }


    function createProductSpaces(inputText) {
        var produtcs = [{"id": "10","value": "Salmão"},{"id": "3","value": "Corvina"},{"id": "6","value": "Pescada"},{"id": "30","value": "Sardinha"}]

        document.getElementById("addProdutos").innerHTML = '';

        for(let i = 0; i<inputText; i++ ){
            const node = `
                <div class="col-6">
                    <div class="input-group my-1 needs-validation py-2">
                        <select id="selectProduct${i}" class="form-select" required> 
                            <option class="is-invalid" disabled selected value="">Selecionar Produto</option>
                        </select><div class="invalid-feedback">Por Favor selecione um produto</div> 
                    </div>
                </div>
            `; 

            document.getElementById("addProdutos").innerHTML += node
        }

        var numChilds =  document.getElementById("addProdutos").childElementCount;

        for (let index = 0; index < numChilds; index++) {
            var selector = document.getElementById("selectProduct"+index);

            produtcs.forEach(element => {
                let newOption = new Option(element.value, element.id);

                selector.add(newOption,undefined);
            });
        }
    }
    
    myModal.toggle();
    myModal.show();

    discardExpoInfo.onclick = (event) =>{
        selectedExpositor.products = [];
        selectedExpositor.capacity = 0;
        selectedExpositor.divisions = 0;
        selectedExpositor.storeSection = 0;
        selectedExpositor.storeSectionColor = '';

    }
}




document.getElementById("addText").onmousedown = (event) =>{
    const myModal = new bootstrap.Modal(document.getElementById('addTextBackdrop'));
    const addTextBtn = document.getElementById('addTextBtn')
    const textInput = document.getElementById('textInput')
    
    addTextBtn.onclick = (event) =>{
        canvas.addTextBlock(new TextBlock(canvas.texts.length,sizeX/2,sizeY/2,textInput.value, 0));
        console.log(textInput.value);
        textInput.value = '';
    }

    CancelTextBtn.onclick = (event) =>{
        textInput.value = '';
    }

    myModal.toggle();
    myModal.show();
}



document.getElementById("CreateMap").onmousedown = (event) =>{
    let array = []
    let index = 0

    const myModal = new bootstrap.Modal(document.getElementById('saveDeleteMap'));
    const myModalTitle = new bootstrap.Modal(document.getElementById('saveDeleteMapTitle'));

    myModalTitle._element.innerText = "Deseja guardar o mapa criado?"

    myModal.toggle();
    myModal.show();

    ConfirmSaveDeleteBtn.onclick = (event) =>{
        console.log("hiiii")
        array[index] = {"width": sizeX,"height": sizeY, "numExpos": canvas.getShapes().length, "numLabels": canvas.getTexts().length};
        index ++;
        
        canvas.getShapes().forEach(element => {
            array[index] = {"id": element.id, "posX": element.posX, "posY": element.posY, "width": element.width,
                            "height": element.height, "color": element.color, "products": element.products, 
                            "capacity": element.capacity, "divisions": element.divisions, 
                            "storeSection": element.storeSection, "storeSectionColor": element.storeSectionColor};
            index ++;
        });

        canvas.getTexts().forEach(element => {
            array[index] = {"id": element.id, "posX": element.posX, "posY": element.posY, "width": element.width,
                            "height": element.height, "angle": element.angle, "value": element.text};
            index ++;
        });

        let json = JSON.stringify(array)
        localStorage.setItem("map",json);
    }
}

    document.getElementById("DeleteMap").onmousedown = (event) =>{
        const myModal = new bootstrap.Modal(document.getElementById('saveDeleteMap'));
        const myModalTitle = new bootstrap.Modal(document.getElementById('saveDeleteMapTitle'));
    
        myModalTitle._element.innerText = "Deseja descartar o mapa criado?"
    
        myModal.toggle();
        myModal.show();

        ConfirmSaveDeleteBtn.onclick = (event) =>{
            canvas.shapes = [];
            canvas.texts = [];
            canvas.draw_shapes();
        }
    }







//https://stackoverflow.com/questions/22785521/how-can-i-drag-a-piece-of-user-generated-text-around-the-html5-canvas

