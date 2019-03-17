

function addToCart(e){
    e.preventDefault();
    const element = e.target;

    const bookId = element.getAttribute('data-book-id');
    const bookType = element.getAttribute('data-book-type');
    const price = element.getAttribute('data-book-price');
    
    url = "add_to_cart/";
    data = { 
        id: bookId,
        type: bookType, 
    };
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify(data)
    })  
    .then(response => response.json())
    .then(response => console.log(response["status"]))
    .then(updateCartDisplay(price))
    .catch(error => alert(error));
}


function updateCartDisplay(price, quantity=1){
    const priceElement = document.querySelector('#cart-price');
    const quantityElement = document.querySelector('#cart-quantity');

    priceElement.textContent = (parseFloat(priceElement.textContent) + parseFloat(price)).toFixed(2);
    quantityElement.textContent = parseInt(quantityElement.textContent) + quantity;

}