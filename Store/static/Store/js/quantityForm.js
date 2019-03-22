
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
    
    const clickedElement = event.currentTarget;
    const previousChoosen = document.querySelector("#choosen");
    previousChoosen.removeAttribute("id");

    clickedElement.setAttribute("id", "choosen");

    const swapableElement = document.querySelector("#swapable");
    const toSwap = clickedElement.firstElementChild;
    
    swapableElement.removeChild(swapableElement.firstElementChild);
    swapableElement.appendChild(toSwap.cloneNode(true));

    const bookId = toSwap.getAttribute("data-book-id");
    const bookType = toSwap.getAttribute("data-book-type");
    const bookPrice = toSwap.getAttribute("data-book-price");
    
    const elementWithDataAttrs = document.querySelector("#add-to-cart");
    elementWithDataAttrs.setAttribute("data-book-id", bookId );
    elementWithDataAttrs.setAttribute("data-book-type", bookType);
    elementWithDataAttrs.setAttribute("data-book-price", bookPrice);


}
