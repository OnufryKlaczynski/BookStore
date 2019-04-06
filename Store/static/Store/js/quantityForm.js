
function changeQuantityValue(quantity){
    const quantityElement = document.querySelector("#quantity");
    if(parseInt(quantityElement.value) + quantity > 0 ){
        quantityElement.value = parseInt(quantityElement.value) + quantity;
    } 
    console.log(quantityElement.value);
}


function addToCartFromInput(event){
    event.preventDefault();
    const inputElement = document.querySelector("#quantity");
    const quantity = parseInt(inputElement.value);
    addToCart(event, quantity);
}


function chooseType(event){
    
    const previousChoosen = document.querySelector("#choosen");
    const clickedElement = event.currentTarget;
    previousChoosen.removeAttribute("id");

    clickedElement.setAttribute("id", "choosen");

    const toSwap = clickedElement.firstElementChild;
    
    const swapableElement = document.querySelector("#swapable");
    swapableElement.removeChild(swapableElement.firstElementChild);
    swapableElement.appendChild(toSwap.cloneNode(true));

    const bookId = toSwap.getAttribute("data-book-id");
    const bookType = toSwap.getAttribute("data-book-type");
    const bookPrice = toSwap.getAttribute("data-book-price");
    
    changeDataValuesOnAddToCartButton(bookId, bookType, bookPrice);

}

function changeDataValuesOnAddToCartButton(bookId, bookType, bookPrice){
    const elementWithDataAttrs = document.querySelector("#add-to-cart");
    elementWithDataAttrs.setAttribute("data-book-id", bookId );
    elementWithDataAttrs.setAttribute("data-book-type", bookType);
    elementWithDataAttrs.setAttribute("data-book-price", bookPrice);

}

const initialSetChoosenProperty = () =>{
    const elements = document.querySelectorAll(".choosable");
    const last_element = elements[elements.length-1];
    last_element.setAttribute("id", "choosen");

    const bookId = last_element.firstElementChild.getAttribute("data-book-id");
    const bookType = last_element.firstElementChild.getAttribute("data-book-type");
    const bookPrice = last_element.firstElementChild.getAttribute("data-book-price");
    
    changeDataValuesOnAddToCartButton(bookId, bookType, bookPrice);

};

initialSetChoosenProperty();