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
        
    def total(self):
        # Get product IDs from the cart
        product_ids = self.cart.keys()
        # Lookup the products in the Product model
        products = Product.objects.filter(id__in=product_ids)
        # Get the quantities from the cart
        quantities = self.cart
        # Initialize total
        total = 0
        for key, value in quantities.items():
            # Convert key to int for comparison
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_offer:
                        # Use offer price if applicable
                        total += product.offer_price * value
                    else:
                        # Otherwise, use the regular price
                        total += product.price * value
        return total
        # returns {'4': 3} product ID and value of the product
        
       
        
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
        

        
