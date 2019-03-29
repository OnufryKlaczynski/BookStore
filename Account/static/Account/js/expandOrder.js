


function expandOrder(event){
    const target = event.currentTarget;
    
    const expandable = target.nextElementSibling;
    
    expandable.classList.toggle("expanded");
        

    
}


let orderElements = document.querySelectorAll(".expandable");

orderElements.forEach( (element) => {
    element.onclick = expandOrder;
});