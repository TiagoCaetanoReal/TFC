import { Expositor } from './expositor.js';

export class Quadro{
    constructor(canvas, context, limits){
        this.canvas = canvas;
        this.context = context;
        
        this.texts = [];
        this.shapes = []; 
        
        this.canvas.width = limits.x;
        this.canvas.height = limits.y;

        this.canvas_width = canvas.width;
        this.canvas_height = canvas.height;
        
        this.current_shape_index = null;
        this.is_dragging;
        this.is_draggingResizer;
        this.is_draggingText;
        
        this.selectedShape;

        this.selectedExpo = false;
        this.selectedText = false;
        this.isMouseOverCanvas = false;

        
        this.startX;
        this.startY;

        this.translateX = 0;
        this.translateY = 0;    

        this.scale = 0.5;
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


    is_mouse_in_shape(x, y, shape){
        var shape_left = shape.posX;
        var shape_right = (shape.posX + shape.width);
        var shape_top = shape.posY;
        var shape_bottom = (shape.posY + shape.height);
        

        if(x > shape_left && x  < shape_right){
            if(y> shape_top && y < shape_bottom){
                return true;
            }   
        }

        return false;
    }

    draw_shapes(){
        this.context.clearRect(0, 0, this.canvas_width, this.canvas_height);
        this.context.save();
        this.context.scale(this.scale,this.scale);

        for(let shape of this.shapes){
            this.context.save();
            this.context.translate(this.translateX, this.translateY);
            this.context.globalAlpha = shape.colorAlpha;
            this.context.fillStyle = shape.color;
            this.context.fillRect(shape.posX, shape.posY, shape.width, shape.height )
            this.context.restore();
        }

        for(let text of this.texts){
            this.context.fillStyle = '#000';

            this.context.save();
            this.context.translate(this.translateX, this.translateY);
            this.context.translate(text.posX - text.width / 2, text.posY - text.height / 2);
            this.context.rotate(text.get_angle() * Math.PI / 180);
            this.context.fillText(text.text, -text.width / 2,  text.height / 4);
            this.context.restore();
        }
        
        this.context.restore();
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
            
            this.is_dragging = true;
           
           
            for( const shape of this.shapes){
                if(this.is_mouse_in_shape((this.startX) / this.scale - this.translateX, (this.startY) / this.scale - this.translateY, shape)){
                    this.current_shape_index = index;
                    this.selectedExpo = true;

                    this.recolor();
                    shape.changeAlpha(0.5)
                    return;
                }
                else{
                    this.selectedExpo = false;
                    this.current_shape_index = null;
                }
                index++;
            }

            this.recolor();
            this.draw_shapes();
        };


        this.canvas.onmouseup = (event) =>{
            if (!this.is_dragging ) {
                return;
            }
            
            event.preventDefault();

            this.is_dragging = false;
            this.draw_shapes(); 
        };

        this.canvas.onmouseout = (event) =>{
            if (!this.is_dragging){
                return;
            } 
            
            event.preventDefault();
             
            this.is_dragging = false;
            this.isMouseOverCanvas = false;
            this.draw_shapes();
        }

        this.canvas.onmousemove = (event) =>{
            if(this.is_dragging){
                const pos = getMousePosition(event);

                event.preventDefault();

                let dx = pos.x - this.startX;
                let dy = pos.y - this.startY;

                this.translateX += dx;
                this.translateY += dy;  

                if(!this.checkLimits()){
                    this.translateX -= dx;
                    this.translateY -= dy;
                }

                this.startX = pos.x;
                this.startY = pos.y;

                this.draw_shapes();
            }
        }

        this.canvas.onmouseover = (event) =>{
            this.isMouseOverCanvas = true;
        }

        window.addEventListener("wheel", (e) => {
            if (!this.isMouseOverCanvas) {
                e.preventDefault();
                return;
              }

            
            var scale = e.deltaY
            if(scale > 0 && this.scale < 2){
                this.scale += 0.5
            }
            else if(scale < 0 && this.scale > 0.5){
                this.scale -= 0.5
            }
            
            this.draw_shapes();
            
        });
    }

    checkLimits(){
        if(this.translateX > -(this.canvas_width*0.65) && this.translateX < this.canvas_width*0.05){
            if(this.translateY >  -(this.canvas_height*0.45) && this.translateY < this.canvas_height*0.05){
                return true;
            }   
        }
        return false;
    }

 
    recolor(){
        for( let shape of this.shapes){
            if(shape.storeSectionColor === ""){
                shape.color = 'grey';
                shape.changeAlpha(1);
            }
            else
                shape.color = shape.storeSectionColor;
                shape.changeAlpha(1);
        }
    }
}



//ao selecionar expositor mostrar produtos