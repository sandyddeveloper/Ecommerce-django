from django.shortcuts import render,get_object_or_404
from .cart import Cart
from Myapp.models import Product
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages



# Create your views here.
def cart_summary (request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.total()
    return render(request, 'cart_summary.html',{ "cart_products": cart_products, "quantities": quantities, 'totals': totals})



def cart_add (request):
    #lets get the cart
    cart = Cart(request)
    # test the post
    if request.POST.get('action') == 'post':
        #get the infomation stuff
        product_id =int( request.POST.get('product_id'))
        product_qty = int( request.POST.get('product_qty'))
        #lookup product in Db
        product = get_object_or_404(Product, id=product_id)
        
        #add the product to cart
        cart.add(product=product, quantity= product_qty )
        
        #Lets get Cart Quantity
        cart_quantity = cart.__len__()
        # return to cart summary page
        # response = JsonResponse({'status':'success','Product Name:': product.name, 'message':'Product added to cart'})
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request, "Item Added To Shopping Cart...")                       
        return response

        
   

# Ensure you have the Product model imported

def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, "Item Deleted From Shopping Cart...")
        return response
    return JsonResponse({'error': 'Invalid request'}, status=40)


      

def cart_update (request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get the Stuffs
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        #Update the Cart
        cart.update(product=product_id, quantity=product_qty)
        
        #Lets get Cart Quantity
        # cart_quantity = cart.__len__()
        
        # return to cart summary page
        # response = JsonResponse({'status':'success','Product Name:': product.name, 'message':'Product added to cart'})
        response = JsonResponse({'qty':product_qty})
        
        return response
    return redirect("cart_summary")


