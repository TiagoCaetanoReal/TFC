export class Marker{
    constructor(posX, posY, width, height ){
        this.posX = posX;
        this.posY = posY;
       
        this.addPosX = 0; 
        this.addPosY = 0;
        
        this.width = width; 
        this.height = height;
 
        this.markerImg = new Image();
        this.markerImg.src = './static/marker.png';
    }

    move_marker(posX, posY){
        this.addPosX = posX; 
        this.addPosY = posY;
        this.posX +=  this.addPosX;
        this.posY += this.addPosY;
    }

    hard_position_marker(posX,posY){
        this.posX = posX;
        this.posY = posY;
    }

}