export class Expositor{
    constructor(id, posX, posY,  width, height, color, products, capacity, divisions, storeSection, storeSectionColor){
        this.id = id;
        this.posX = posX;
        this.posY = posY;
        this.width = width; 
        this.height = height;
        this.color = color; 

        this.colorAlpha = 1;
        this.products = this.setValue(products, 'array');
        this.capacity = this.setValue(capacity);
        this.divisions = this.setValue(divisions);
        this.storeSection = this.setValue(storeSection);
        this.storeSectionColor = this.setValue(storeSectionColor, 'string');

        console.log(products)
        console.log(capacity)
        this.addPosX = 0; 
        this.addPosY = 0;
    }

    setValue(value, type){
        if(value !== undefined)
            return value;
        else if(value === undefined && type === 'array')
            return [];
        else if(value === undefined && type === 'string')
            return '';
        else
            return 0;
    }

    setProducts(products){
        if(products !== undefined)
            return products
        return [];
    }
    setCapacity(capacity){
        if(capacity !== undefined)
            return capacity
        return 0;
    }
    setDivisions(divisions){
        if(divisions !== undefined)
            return divisions
        return 0;
    }
    setStoreSection(storeSection){
        if(storeSection !== undefined)
            return storeSection
        return 0;
    }
    setStoreSectionColor(storeSectionColor){
        if(storeSectionColor !== undefined)
            return storeSectionColor
        return '';
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