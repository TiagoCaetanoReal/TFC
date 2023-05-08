import { Expositor } from './expositor.js';

export class Quadro{
    constructor(canvas, context){
        this.canvas = canvas;
        this.context = context;
        
        this.texts = [];
        this.shapes = [];
        this.resizeShapes = [];
        
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight ;

        this.canvas_width = canvas.width;
        this.canvas_height = canvas.height;
        
        this.current_shape_index = null;
        this.is_dragging;
        this.is_draggingResizer;
        this.is_draggingText;
        
        this.selectedShape;

        this.selectedExpo = false;
        this.selectedText = false;

        this.resizeCanvas = this.resizeCanvas.bind(this);
        
        this.startX;
        this.startY;
    }
    
    
    addExpositores(expositor){
        this.shapes.push(expositor);
        this.draw_shapes();  
    }
    
    addTextBlock(text){
        this.context.font = "20px arial";
        text.set_height(30);
        text.set_width(this.context.measureText(text.text).width);

        this.texts.push(text);
        this.draw_shapes(); 
    }

    excludeExpositores(id){
        var shape = this.getShapes().find(item => item.id === id);
        const index = this.getShapes().indexOf(shape);
        
        if (index > -1) {  
            this.getShapes().splice(index, 1);
        }
    }
    
    excludeText(id){
        console.log(id)
        var text = this.getTexts().find(item => item.id === id);
        console.log(text)
        const index = this.getTexts().indexOf(text);
        console.log(index)
        
        if (index > -1) {  
            this.getTexts().splice(index, 1);
        }
        console.log(this.getTexts())
    }

    resizers(id){
        var shape = this.getShapes().find(item => item.id === id);
        const index = this.getShapes().indexOf(shape);
        
        this.selectedShape = shape;
        this.resizeShapes = [];

        this.resizeShapes.push(
        new Expositor(0,this.shapes[index].posX+(this.shapes[index].width/2)-5, this.shapes[index].posY-5, 10, 10, 'grey'),
        new Expositor(1,this.shapes[index].posX-5, this.shapes[index].posY+(this.shapes[index].height/2)-5, 10, 10, 'grey'),
        new Expositor(2,this.shapes[index].posX+(this.shapes[index].width/2)-5, this.shapes[index].posY+this.shapes[index].height-5, 10, 10, 'grey'),
        new Expositor(3,this.shapes[index].posX+this.shapes[index].width-5, this.shapes[index].posY+(this.shapes[index].height/2)-5, 10, 10, 'grey'))
    }

    rotateText(selectedText){
        // https://www.youtube.com/watch?v=5vxygxshTQ4
        // para rodar texto, tenho de rodar o canvas todo primeiro 
        // ou seja tenha de roda-lo, adicionar o texto, e colocar os outro ojeto de seguida
        
        selectedText.set_angle(90);
        this.draw_shapes();
    }
    
    getShapes(){
        return this.shapes;
    }

    getTexts(){
        return this.texts;
    }

    getSelected(object){
        return object[this.current_shape_index].id
    }
    
    getCurrentExpositor(){
        return this.shapes[this.current_shape_index]
    }

    
    is_mouse_in_shape(x, y, shape, type){

        let shape_left;
        let shape_right;

        let shape_top;
        let shape_bottom;

        var textLenghts = [];

        if(type === 'text'){
            textLenghts = shape.sizesFromAngle(shape);

            // tentando mudar a seleção do texto, para que quando este rode, a seleção do rato se adapte à rotação
            
            shape_left = textLenghts[0];
            shape_right = textLenghts[1];
            shape_top = textLenghts[2];
            shape_bottom = textLenghts[3];

           
            // shape_left = shape.posX - shape.width/2;
            // shape_right = (shape.posX + shape.width/2);
            // shape_top = shape.posY - shape.height;
            // shape_bottom = shape.posY - shape.height/2;
        }else{
            shape_left = shape.posX;
            shape_right = (shape.posX + shape.width);
            shape_top = shape.posY;
            shape_bottom = (shape.posY + shape.height);
        }

        console.log(textLenghts[0])
        console.log(textLenghts[1])
        console.log(textLenghts[2])
        console.log(textLenghts[3])

        if(x > shape_left && x < shape_right){
            console.log('horz');
            if(y > shape_top && y < shape_bottom){
                console.log(shape.id)
                console.log('vert')
                textLenghts = [];
                return true;
            }   
        }

        return false;
    }

    draw_shapes(){
        this.context.clearRect(0, 0, this.canvas_width, this.canvas_height);

        for(let shape of this.shapes){
            this.context.fillStyle = shape.color;
            this.context.fillRect(shape.posX, shape.posY, shape.width, shape.height )
        }

        for(let shape of this.resizeShapes){
            this.context.fillStyle = 'grey';
            this.context.fillRect(shape.posX, shape.posY, shape.width, shape.height )
        }
 
        console.log(this.texts)
        for(let text of this.texts){
            this.context.fillStyle = '#000';

            // this.resizeShapes.push(
            //     new Expositor(3,text.posX - text.width / 1.5, text.posY - text.height * 1.5, text.height, text.width, 'grey'))

            this.context.save();
            this.context.translate(text.posX - text.width / 2, text.posY - text.height / 2);
            this.context.rotate(text.get_angle() * Math.PI / 180);
            this.context.fillText(text.text, -text.width / 2,  text.height / 4);

            this.context.restore();
        }

        if(this.resizeShapes!=[] && !this.is_draggingResizer && this.is_dragging){
            this.resizeShapes = [];
        }
    }

    resizeCanvas(){
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.draw_shapes();
    }

    detectAction(){
        const getMousePosition = (event) => {
            const rect = this.canvas.getBoundingClientRect();
            const scaleX = this.canvas.width / rect.width;
            const scaleY = this.canvas.height / rect.height;
            return {
                x: (event.clientX - rect.left) * scaleX,
                y: (event.clientY - rect.top) * scaleY
            }
        }

        this.canvas.onmousedown = (event) =>{
            event.preventDefault();

            let mouseX = parseInt(event.clientX);
            let mouseY = parseInt(event.clientY);
            let canvasRect = canvas.getBoundingClientRect();
            this.startX = (mouseX - canvasRect.left) * (this.canvas.width / canvasRect.width);
            this.startY = (mouseY - canvasRect.top) * (this.canvas.height / canvasRect.height);
 
            let index = 0;

            console.log(this.startX + " " + this.startY)

            for( let shape of this.resizeShapes){
                if(this.is_mouse_in_shape(this.startX, this.startY, shape, 're')){
                    this.current_shape_index = shape.id;
                    this.is_dragging = false;
                    this.is_draggingText = false;
                    this.is_draggingResizer= true;
                    this.selectedExpo = false;
                    this.selectedText = false;
                    return;
                }
                else{
                    this.selectedExpo = false;
                    this.selectedText = false;
                    this.current_shape_index = null;
                }
            }

    
            for( let shape of this.shapes){
                if(this.is_mouse_in_shape(this.startX, this.startY, shape, 'exp')){
                    this.current_shape_index = index;
                    this.is_dragging = true;
                    this.is_draggingText = false;
                    this.is_draggingResizer= false;
                    this.selectedExpo = true;
                    this.selectedText = false;
                    this.recolor();
                    shape.color = 'silver';
                    return;
                }
                else{
                    this.selectedExpo = false;
                    this.selectedText = false;
                    this.current_shape_index = null;
                }
                index++;
            }

            index = 0;

            for(let text of this.texts){
                console.log(this.startX+ " " + this.startY)
                console.log(text)

                if(this.is_mouse_in_shape(this.startX, this.startY, text, 'text')){
                    this.current_shape_index = index;
                    console.log(this.current_shape_index)
                    this.is_dragging = false;
                    this.is_draggingResizer= false;
                    this.is_draggingText = true;
                    this.selectedExpo = false;
                    this.selectedText = true;
                    return
                }
                else{
                    this.selectedExpo = false;
                    this.selectedText = false;
                    this.current_shape_index = null;
                }
                index++;
            }
            
            this.recolor();
            this.draw_shapes();
        };


        this.canvas.onmouseup = (event) =>{
            if (!this.is_dragging && !this.is_draggingResizer && !this.is_draggingText) {
                return;
            }
            
            event.preventDefault();

            this.is_dragging = false;
            this.is_draggingResizer= false;
            this.is_draggingText= false;
            this.draw_shapes(); 
        };

        this.canvas.onmouseout = (event) =>{
            if (!this.is_dragging && !this.is_draggingResizer && !this.is_draggingText){
                return;
            } 
            
            event.preventDefault();
             
            this.is_dragging = false;
            this.is_draggingResizer= false;
            this.is_draggingText = false;
            this.draw_shapes();
        }

        this.canvas.onmousemove = (event) =>{
            if (!this.is_dragging && this.is_draggingResizer && !this.is_draggingText) {
                const pos = getMousePosition(event);
                this.moveShapes(event, this.resizeShapes, pos);
                this.resize(this.resizeShapes[this.current_shape_index], this.selectedShape);

                this.resizeShapes[0].hard_position_expositor(this.selectedShape.posX+(this.selectedShape.width/2)-5, this.selectedShape.posY-5)
                this.resizeShapes[1].hard_position_expositor(this.selectedShape.posX-5, this.selectedShape.posY+(this.selectedShape.height/2)-5)
                this.resizeShapes[2].hard_position_expositor(this.selectedShape.posX+(this.selectedShape.width/2)-5, this.selectedShape.posY+this.selectedShape.height-5)
                this.resizeShapes[3].hard_position_expositor(this.selectedShape.posX+this.selectedShape.width-5, this.selectedShape.posY+(this.selectedShape.height/2)-5)
       
            }else if(this.is_dragging && !this.is_draggingResizer && !this.is_draggingText){
                const pos = getMousePosition(event);
                this.moveShapes(event, this.shapes, pos)

            }else if(!this.is_dragging && !this.is_draggingResizer && this.is_draggingText){
                const pos = getMousePosition(event);
                this.moveText(event, this.texts, pos)

            }
            else{
                return;
            }
        }
    }

    resize(selectedShape, selectedExpositor){
        if((selectedShape.id % 2) == 0){
            selectedExpositor.resize_expositor(0,this.resizeShapes[this.current_shape_index].addPosY)
        }
        else{ 
            selectedExpositor.resize_expositor(this.resizeShapes[this.current_shape_index].addPosX,0)
        }

        if(selectedExpositor.width < 10){
            selectedExpositor.width =10;
        }else if(selectedExpositor.height < 10){
            selectedExpositor.height =10;
        }
        this.draw_shapes();

     }

    // trying to move text
    moveShapes(event, shapeList, pos){
        event.preventDefault();

        let dx = pos.x - this.startX;
        let dy = pos.y - this.startY;

        let current_shape = shapeList[this.current_shape_index];
        current_shape.move_expositor(dx, dy);
    
        this.draw_shapes();

        this.startX = pos.x;
        this.startY = pos.y;
    }

    moveText(event, textList, pos){
        event.preventDefault();

        let dx = pos.x - this.startX;
        let dy = pos.y - this.startY;

        let current_shape = textList[this.current_shape_index];
        current_shape.move_text(dx, dy);
    
        this.draw_shapes();

        this.startX = pos.x;
        this.startY = pos.y;
    }

    recolor(){
        for( let shape of this.shapes){
            if(shape.storeSectionColor === "")
                shape.color = 'grey';
            else
                shape.color = shape.storeSectionColor;
        }
    }
}

// cubos de resize ficam agarrados ao rato, resolver isso depois fazer função para verificar o id de qual o square que esta a ser segurado para fazer o resize só pela sua lateral
