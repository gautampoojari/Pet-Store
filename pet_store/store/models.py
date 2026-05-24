from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    
    def __str__(self):
        return self.first_name,self.last_name
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='uploads/product')
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=200,null=False,blank=False)
    phone=models.CharField(max_length=20)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.product
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str___(self):
        return str(self.user)