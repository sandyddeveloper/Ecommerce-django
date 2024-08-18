from Myapp.models  import Product
class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #Get the current session key if its extits
        cart = self.session.get('session_key')
        
        
        #If not, create a new one
        if  'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        #lets make sure that cart is available on all the pages of application
        self.cart = cart
        
    def add(self, product):
        product_id = str(product.id)
        
        #Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {
                'price': str(product.price),
            }
            
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in DB model
        products = Product.objects.filter(id__in = product_ids) # Here __in menas checking the django ORM whether it persent or not
        # Return products
        return products