
function addToCart(e, quantity=1){
    e.preventDefault();
    const element = e.target;

    const bookId = element.getAttribute('data-book-id');
    const bookType = element.getAttribute('data-book-type');
    const price = element.getAttribute('data-book-price');
    
    data = { 
        id: bookId,
        type: bookType,
        quantity: quantity,
    };
    postDataToCartView(data);
    updateCartDisplay(price, quantity);
}

function postDataToCartView(data){
    const baseUrl = window.location.origin;
    const url = "/store/add_to_cart/";

    fetch(baseUrl+url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify(data)
    })  
    .then(response => response.json())
    .then(response => console.log(response["status"], response['error_msg']))
    .catch(error => alert(error));
}


function updateCartDisplay(price, quantity){
    console.log(price, quantity);
    const priceElement = document.querySelector('#cart-price');
    const quantityElement = document.querySelector('#cart-quantity');

    priceElement.textContent = (parseFloat(priceElement.textContent) + parseFloat(price)).toFixed(2) + "PLN";
    quantityElement.textContent = parseInt(quantityElement.textContent) + quantity;

}