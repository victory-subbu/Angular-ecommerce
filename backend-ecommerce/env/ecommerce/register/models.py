from django.db import models
from django.conf import settings
import os
# Create your models here.

def product_images(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'product_images', filename)

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
    productname = models.CharField(max_length=255)
    productprice = models.DecimalField(max_digits=10, decimal_places=2)
    productcolor = models.CharField(max_length=100)
    productcategory = models.CharField(max_length=100)
    productdescription = models.TextField()
    productimage = models.FileField(blank=True,null=True,upload_to=product_images)




