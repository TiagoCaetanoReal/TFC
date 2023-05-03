import { Expositor } from './expositor.js';
import { Quadro } from './quadro.js';

// https://www.youtube.com/watch?v=7PYvx8u_9Sk

let canvas = new Quadro(document.getElementById("canvas"), document.getElementById("canvas").getContext("2d"));
canvas.detectAction();
let sizeX = canvas.canvas_width;
let sizeY = canvas.canvas_height;

// Adiciona o listener de resize à janela do navegador
// window.addEventListener("resize", canvas.resizeCanvas, false);


document.getElementById("addExpositor").onmousedown = (event) =>{
    canvas.addExpositores(new Expositor(canvas.shapes.length,sizeX/2,sizeY/2, 20, 60, 'grey'));
}

document.getElementById("rotateExpositor").onmousedown = (event) =>{
    try {
        canvas.getShapes()[canvas.getSelectedExpositor()].rotate_expositor();
        canvas.reziseShapes = [];
    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação");
    }
    
    canvas.draw_shapes();
}

document.getElementById("excludeExpositor").onmousedown = (event) =>{ 
    try {
        canvas.excludeExpositores(canvas.getSelectedExpositor())
        canvas.reziseShapes = [];
    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação"); 
    }
    
    canvas.draw_shapes();
}

document.getElementById("resizeExpositor").onmousedown = (event) =>{
    try {
        let selectedExpositor = canvas.getSelectedExpositor()
        canvas.resizers(selectedExpositor)
    } catch (error) {
        window.alert("Selecione um expositor para realizar esta ação"); 
    }
    
    canvas.draw_shapes();
}

document.getElementById("detailExpositor").onmousedown = (event) =>{
    let selectedExpositor;
    try {
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

        // resolver facto de produtos que aparecem no expositor, serem do expositor editado anteriormente 

        //nesta parte após serem criados os selects dos produtos, tem de ser mandado do backend um array ou string com os produtos, possivelmente um array
    }

    
    document.getElementById('selectSector').onchange = (event) => {
        var inputText = event.target.value;
        selectedExpositor.storeSection = parseInt(inputText);
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
    // saveInfo id do botão de salvar modal

    
    myModal.toggle();
    myModal.show();
}


document.getElementById("CreateMap").onmousedown = (event) =>{
    let array = []
    let index = 0
    canvas.getShapes().forEach(element => {
        array[index] = {"id": element.id, "posX": element.posX/sizeX, "posY": element.posY/sizeY, "width": element.width/sizeX,
                        "height": element.height/sizeY, "color": element.color, "products": element.products, 
                        "capacity": element.capacity, "divisions": element.divisions, "storeSection": element.storeSection};
        index ++;
    });

    let json = JSON.stringify(array)
    localStorage.setItem("map",json);
}


/* adicionar função de adicionar bloco de texto
document.getElementById("addText").onmousedown = (event) =>{
    console.log(canvas.getShapes()[canvas.getSelectedExpositor()])
    canvas.getShapes()[canvas.getSelectedExpositor()].rotate_expositor();
    canvas.draw_shapes();
}

*/
