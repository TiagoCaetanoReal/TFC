export class TextBlock{
    constructor(id, posX, posY, text){
        this.id = id;
        this.posX = posX;
        this.posY = posY;
        this.text = text;
        this.width; 
        this.height;
        this.angle = 0;

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
    
    set_angle(angle){
        if(this.angle === 270)
            angle = -270;

        this.angle += angle; 
    }

    get_angle(){return this.angle }

    sizesFromAngle(obj){
        var textLenghts = [];
        let width = obj.width;
        let height = obj.height;

        if(obj.angle === 90 || obj.angle === 270){
            textLenghts[0] = obj.posX - width / 1.5;
            textLenghts[1] = textLenghts[0] + height;
            textLenghts[2] = obj.posY - height * 1.5;
            textLenghts[3] = textLenghts[2] + width;
        } 
       
        else{
            textLenghts[0] = obj.posX - width;
            textLenghts[1] = (obj.posX + width/2);
            textLenghts[2] = obj.posY - height;
            textLenghts[3] = obj.posY + height/2;
        }
        return textLenghts;
    }
}