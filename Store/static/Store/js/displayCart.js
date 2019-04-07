function changeValue(event){
    const elementClicked = event.currentTarget;
    let quantity = 0;
    let quantityElement;

    if(elementClicked.id === "remove-icon"){
        quantity = -1;
        quantityElement = elementClicked.nextElementSibling;
    }else if(elementClicked.id === "add-icon"){
        quantity = 1;
        quantityElement = elementClicked.previousElementSibling;
    }
    else{
        return
    }

    if(parseInt(quantityElement.innerText)<1 && quantity<1){
        return;
    }
    quantityElement.innerText = quantity + parseInt(quantityElement.innerText);

    const dataElement = elementClicked.parentElement;
    const bookId = dataElement.getAttribute("data-book-id");
    const bookType = dataElement.getAttribute("data-book-type");
    const price = dataElement.getAttribute("data-book-price");

    data = { 
        id: bookId,
        type: bookType,
        quantity: quantity,
    };

    postDataToCartView(data);   
    updateCartDisplay(price, quantity);

    // update total-price element
    // TODO: move it to its own function
    for(let element of dataElement.parentElement.children){
        if(element.classList.contains("total-price") === true){
            
            element.innerText = (parseFloat(element.innerText) + (price*quantity)).toFixed(2) +"PLN";
        }
    }

}



const quantityChangeElements = document.querySelectorAll(".quantity-change");
quantityChangeElements.forEach(element => {
    element.children[0].onclick = changeValue;
    element.children[2].onclick = changeValue;
});

