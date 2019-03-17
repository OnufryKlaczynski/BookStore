from .cart import Cart

def cart(request):
    cart = Cart(request)
    price = cart.get_total_price()
    quantity = 0
    cart = {"price":price, "quantity":quantity}
    return {'cart' : cart}