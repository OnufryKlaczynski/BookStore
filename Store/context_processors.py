from .cart import Cart

def cart(request):
    cart = Cart(request.session)
    price, quantity = cart.get_total_price_and_quantity()
    global_cart = {"price":price, "quantity":quantity}
    return {'global_cart' : global_cart}