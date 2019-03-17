from .cart import Cart

def cart(request):
    cart = Cart(request)
    price, quantity = cart.get_total_price_and_quantity()
    cart = {"price":price, "quantity":quantity}
    return {'cart' : cart}