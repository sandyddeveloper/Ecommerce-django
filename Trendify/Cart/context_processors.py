from .cart import Cart

# Create a context processor so our cart can work on all pathforms
def  cart(request):
    return {'cart': Cart(request)}