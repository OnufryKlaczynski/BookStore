
function addToCart(e, quantity=1){
    e.preventDefault();
    const element = e.target;

    const bookId = element.getAttribute('data-book-id');
    const bookType = element.getAttribute('data-book-type');
    const price = element.getAttribute('data-book-price');
    const baseUrl = window.location.origin;
    const url = "/store/add_to_cart/";
    data = { 
        id: bookId,
        type: bookType,
        quantity: quantity,
    };
    fetch(baseUrl+url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify(data)
    })  
    .then(response => response.json())
    .then(response => console.log(response["status"]))
    .then(updateCartDisplay(price, quantity))
    .catch(error => alert(error));
}


function updateCartDisplay(price, quantity){
    const priceElement = document.querySelector('#cart-price');
    const quantityElement = document.querySelector('#cart-quantity');

    priceElement.textContent = (parseFloat(priceElement.textContent) + parseFloat(price)).toFixed(2);
    quantityElement.textContent = parseInt(quantityElement.textContent) + quantity;

}