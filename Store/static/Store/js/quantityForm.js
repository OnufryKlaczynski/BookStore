
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