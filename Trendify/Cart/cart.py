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
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {
            #     'price': str(product.price),
            # }
            self.cart[product_id] =  int (product_qty)
            
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
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,  product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #the explaination of above function id  { '4': 3}
        #Get the Cart
        ourcart = self.cart
        
        #Lets update the Dictionary/cart
        ourcart[product_id] = product_qty
        
        #Update the session
        self.session['cart'] = ourcart
        
        #Mark the session as modified
        self.session.modified = True
        
        allproducts = self.cart
        return allproducts
        
    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        
