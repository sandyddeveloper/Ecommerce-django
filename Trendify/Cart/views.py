from django.shortcuts import render,get_object_or_404
from .cart import Cart
from Myapp.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary (request):
    return render(request, 'cart_summary.html',{ })



def cart_add (request):
    #lets get the cart
    cart = Cart(request)
    # test the post
    if request.POST.get('action') == 'post':
        #get the infomation stuff
        product_id =int( request.POST.get('product_id'))
        #lookup product in Db
        product = get_object_or_404(Product, id=product_id)
        #add the product to cart
        cart.add(product=product)
        
        #Lets get Cart Quantity
        cart_quantity = cart.__len__()
        # return to cart summary page
        # response = JsonResponse({'status':'success','Product Name:': product.name, 'message':'Product added to cart'})
        response = JsonResponse({'qty':cart_quantity})
                                
        return response

        
   


def cart_delete (request):
    pass


def cart_update (request):
    pass