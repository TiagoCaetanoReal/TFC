export class Expositor{
    constructor(id, posX, posY,  width, height, color){
        this.id = id;
        this.posX = posX;
        this.posY = posY;
        this.width = width; 
        this.height = height;
        this.color = color; 

        this.colorAlpha = 1;
        this.products = [];
        this.capacity = 0;
        this.divisions = 0;
        this.storeSection = 0;
        this.storeSectionColor = '';

        this.addPosX = 0; 
        this.addPosY = 0;
    }

    changeAlpha(value){
        this.colorAlpha = value;
    }
    
    give_colorSection(color){
        this.storeSectionColor = color;
        this.color = this.storeSectionColor;
        console.log(color)
        console.log(this.storeSectionColor)
        console.log(this.color)
    }

    reColor_Expositor(){
        this.color = this.storeSectionColor;
    }

    move_expositor(posX, posY){
        this.addPosX = posX; 
        this.addPosY = posY;
        this.posX +=  this.addPosX;
        this.posY += this.addPosY;
    }

    rotate_expositor(){
        let tempSize = this.width;
        this.width = this.height;
        this.height = tempSize;
    }

    resize_expositor(widthAddition,heightAddition){
        this.width += widthAddition;
        this.height += heightAddition;
    }

    hard_position_expositor(posX,posY){
        this.posX = posX;
        this.posY = posY;
    }

}