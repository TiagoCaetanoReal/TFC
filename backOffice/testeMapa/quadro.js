import { Expositor } from './expositor.js';

export class Quadro{
    constructor(canvas, context){
        this.canvas = canvas;
        this.context = context;
        
        this.texts = [];
        this.shapes = [];
        this.reziseShapes = [];
        
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight ;

        this.canvas_width = canvas.width;
        this.canvas_height = canvas.height;
        
        this.current_shape_index = null;
        this.is_dragging;
        this.is_draggingResizer;
        this.selectedShape;

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
        text.set_height(16);
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

    resizers(id){
        var shape = this.getShapes().find(item => item.id === id);
        const index = this.getShapes().indexOf(shape);
        
        this.selectedShape = shape;

        this.reziseShapes = [];

        this.reziseShapes.push(
        new Expositor(0,this.shapes[index].posX+(this.shapes[index].width/2)-5, this.shapes[index].posY-5, 10, 10, 'grey'),
        new Expositor(1,this.shapes[index].posX-5, this.shapes[index].posY+(this.shapes[index].height/2)-5, 10, 10, 'grey'),
        new Expositor(2,this.shapes[index].posX+(this.shapes[index].width/2)-5, this.shapes[index].posY+this.shapes[index].height-5, 10, 10, 'grey'),
        new Expositor(3,this.shapes[index].posX+this.shapes[index].width-5, this.shapes[index].posY+(this.shapes[index].height/2)-5, 10, 10, 'grey'))
    }

    

    getShapes(){
        return this.shapes;
    }

    getSelectedExpositor(){
        return this.shapes[this.current_shape_index].id
    }
    
    getCurrentExpositor(){
        return this.shapes[this.current_shape_index]
    }

    
    is_mouse_in_shape(x, y, shape){
        let shape_left = shape.posX;
        let shape_right = (shape.posX + shape.width);
        let shape_top = shape.posY;
        let shape_bottom = (shape.posY + shape.height);
        
        if(x > shape_left && x < shape_right){
            if(y > shape_top && y < shape_bottom){
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

        for(let shape of this.reziseShapes){
            this.context.fillStyle = shape.color;
            this.context.fillRect(shape.posX, shape.posY, shape.width, shape.height )
        }

        for(let text of this.texts){
            // this.context.fillStyle = shape.color;
            // this.context.fillRect(shape.posX, shape.posY, shape.width, shape.height )
            this.context.fillText(text.text,text.posX,text.posY);
        }

        if(this.reziseShapes!=[] && !this.is_draggingResizer && this.is_dragging){
            this.reziseShapes = [];
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

            for( let shape of this.reziseShapes){

                if(this.is_mouse_in_shape(this.startX, this.startY, shape)){
                    this.current_shape_index = shape.id;
                    this.is_dragging = false;
                    this.is_draggingResizer= true;
                    
                    return;
                }
                else{
                    this.current_shape_index = null;
                }
                
            }

    
            for( let shape of this.shapes){

                if(this.is_mouse_in_shape(this.startX, this.startY, shape)){
                    this.current_shape_index = index;
                    this.is_dragging = true;
                    this.is_draggingResizer= false;
                    this.recolor();
                    shape.color = 'silver';
                    return;
                }
                else{
                    this.current_shape_index = null;
                }

                index++;
            }
            
            this.recolor();
            this.draw_shapes();
        };


        this.canvas.onmouseup = (event) =>{
            if (!this.is_dragging && !this.is_draggingResizer) {
                return;
            }
            
            event.preventDefault();

            this.is_dragging = false;
            this.is_draggingResizer= false;
            this.draw_shapes(); 
        };

        this.canvas.onmouseout = (event) =>{
            if (!this.is_dragging && !this.is_draggingResizer){
                return;
            } 
            
            event.preventDefault();
             
            this.is_dragging = false;
            this.is_draggingResizer= false;
            this.draw_shapes();
        }

        this.canvas.onmousemove = (event) =>{
            if (!this.is_dragging && this.is_draggingResizer) {
                const pos = getMousePosition(event);
                this.moveShapes(event, this.reziseShapes, pos);
                this.rezise(this.reziseShapes[this.current_shape_index], this.selectedShape);

                this.reziseShapes[0].hard_position_expositor(this.selectedShape.posX+(this.selectedShape.width/2)-5, this.selectedShape.posY-5)
                this.reziseShapes[1].hard_position_expositor(this.selectedShape.posX-5, this.selectedShape.posY+(this.selectedShape.height/2)-5)
                this.reziseShapes[2].hard_position_expositor(this.selectedShape.posX+(this.selectedShape.width/2)-5, this.selectedShape.posY+this.selectedShape.height-5)
                this.reziseShapes[3].hard_position_expositor(this.selectedShape.posX+this.selectedShape.width-5, this.selectedShape.posY+(this.selectedShape.height/2)-5)
       
            }else if(this.is_dragging && !this.is_draggingResizer){
                const pos = getMousePosition(event);
                this.moveShapes(event, this.shapes, pos)

            }else{
                return;
            }
        }
    }

    rezise(selectedShape, selectedExpositor){
        if((selectedShape.id % 2) == 0){
            selectedExpositor.rezise_expositor(0,this.reziseShapes[this.current_shape_index].addPosY)
        }
        else{ 
            selectedExpositor.rezise_expositor(this.reziseShapes[this.current_shape_index].addPosX,0)
        }

        if(selectedExpositor.width < 10){
            selectedExpositor.width =10;
        }else if(selectedExpositor.height < 10){
            selectedExpositor.height =10;
        }
        this.draw_shapes();

     }
    
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

    recolor(){
        for( let shape of this.shapes){
            
            if(shape.storeSectionColor === "")
                shape.color = 'grey';
            else
                shape.color = shape.storeSectionColor;
        }
    }
}

// cubos de rezise ficam agarrados ao rato, resolver isso depois fazer função para verificar o id de qual o square que esta a ser segurado para fazer o rezise só pela sua lateral
