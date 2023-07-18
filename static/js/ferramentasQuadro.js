import { Expositor } from './expositor.js';
 
export function excludeExpositores(shapes, id){  
    var shape = shapes.find(item => item.id === id);
    const index = shapes.indexOf(shape);
     
    if (index > -1) { 
        shapes.splice(index, 1);

        // Atualiza os IDs dos objetos que foram adicionados a seguir ao expositor que for removido
        for (let i = index; i < shapes.length; i++) { 
            shapes[i].id--;
        }
    } 
 
    return shapes
}

export function excludeText(texts, id){
    var text = texts.find(item => item.id === id);
    const index = texts.indexOf(text);
    
    if (index > -1) {  
        texts.splice(index, 1);

        // Atualiza os IDs dos objetos que foram adicionados a seguir ao texto que for removido
        for (let i = index; i < texts.length; i++) {
            texts[i].id--;
        }
    }
    return texts
}

export function resizers(shapes, resizers, id){
    
    var shape = shapes.find(item => item.id === id); 
    
    resizers = [];

    resizers.push(
    new Expositor(0,shape.posX+(shape.width/2)-5, shape.posY-5, 10, 10, 'grey'),
    new Expositor(1,shape.posX-5, shape.posY+(shape.height/2)-5, 10, 10, 'grey'),
    new Expositor(2,shape.posX+(shape.width/2)-5, shape.posY+shape.height-5, 10, 10, 'grey'),
    new Expositor(3,shape.posX+shape.width-5, shape.posY+(shape.height/2)-5, 10, 10, 'grey'))
 
    return [shape, resizers];
} 

export function recolor(shapes){
    for( let shape of shapes){
        if(shape.storeSectionColor === ""){
            shape.color = 'grey';
            shape.changeAlpha(1);
        }
        else
            shape.color = shape.storeSectionColor;
            shape.changeAlpha(1);
    }
}