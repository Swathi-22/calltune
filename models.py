from django.db import models
from django.db.models.base import Model
from django.utils.tree import Node

from web.views import product_details_view

class category(models.Model):
    
    category = models.CharField(max_length=100,null=False,unique=True)
    category_image = models.ImageField(upload_to = 'category_image')


    def __str__(self):
        return self.category



class brand(models.Model):

    brand_name = models.CharField(max_length=50)

    
    def __str__(self):
        return self.brand_name

class product_model(models.Model):

    category = models.ForeignKey(category,on_delete=models.CASCADE)
    brand = models.ForeignKey(brand,on_delete=models.CASCADE,)
    model_name = models.CharField(max_length=50)

    def __str__(self):
        return self.model_name




class product(models.Model):

    date = models.DateField(auto_now_add=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    model = models.ForeignKey(product_model, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to = 'product_image')
    price = models.IntegerField()

    def __str__(self):
        return self.product_name


class cart(models.Model):
    date = models.DateField(auto_now_add=True)
    session_key = models.CharField(max_length=1000)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()



