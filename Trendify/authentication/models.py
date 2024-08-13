from django.db import models
import datetime
# Create your models here.

class Customer(models.Model):
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    phone =models.CharField(max_length=10)
    email =models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class  Meta:
        verbose_name_plural = 'categories'
    
    
#All of our Products

class Product(models.Model):
    id =models.AutoField
    name = models.CharField(max_length=200, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=300, default='', blank=True, null=True)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images/', default="")
    #Add sales information
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    def __str__(self):
        return self.name
    
    #Customer Order Details
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    date =  models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product
    