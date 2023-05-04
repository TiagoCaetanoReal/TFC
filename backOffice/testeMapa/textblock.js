export class TextBlock{
    constructor(id, posX, posY, text){
        this.id = id;
        this.posX = posX;
        this.posY = posY;
        this.text = text;
        this.width; 
        this.height;

        this.addPosX = 0; 
        this.addPosY = 0;
    }
    
    move_text(posX, posY){
        this.addPosX = posX; 
        this.addPosY = posY;
        this.posX +=  this.addPosX;
        this.posY += this.addPosY;
    }

    set_width(width){
        this.width = width; 
    }

    set_height(height){
        this.height = height;
    }
    
}