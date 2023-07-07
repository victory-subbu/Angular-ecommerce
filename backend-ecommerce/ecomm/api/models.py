from django.db import models
# Create your models here.
from django.conf import settings
import os
import uuid
# Create your models here.

def product_images(instance, filename):
    return '/'.join(['product_images',filename])
    

class CustomerSignup(models.Model):
    userid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    phonenumber=models.IntegerField()
    address=models.CharField(max_length=255)

class SellerSignup(models.Model):
    sellerid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    phonenumber=models.IntegerField()
    address=models.CharField(max_length=255)

class Product(models.Model):
    seller = models.ForeignKey(SellerSignup, on_delete=models.CASCADE, related_name='products')
    productid=models.AutoField(primary_key=True)
    productname = models.CharField(max_length=255)
    productprice = models.DecimalField(max_digits=10, decimal_places=2)
    productcolor = models.CharField(max_length=100)
    productcategory = models.CharField(max_length=100)
    productdescription = models.TextField()
    productimage = models.FileField(blank=True,null=True,upload_to=product_images)


class Cart(models.Model):
    customer = models.ForeignKey(CustomerSignup, on_delete=models.CASCADE)
    cartid=models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_color = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_description = models.TextField()
    product_image = models.FileField(blank=True, null=True, upload_to='product_images')

class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerSignup, on_delete=models.CASCADE)
    cartid=models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_color = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_description = models.TextField()
    product_image = models.FileField(blank=True, null=True, upload_to='product_images')
    order_date = models.DateTimeField(auto_now_add=True)
