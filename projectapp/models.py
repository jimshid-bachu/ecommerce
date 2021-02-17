from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ProfilePic(models.Model):
    pic = models.ImageField(upload_to = 'profilepics')
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'ProfilePic'
        verbose_name = 'pic'
        verbose_name_plural = 'pics'    
    def __str__(self):
        return self.user.username


class Products(models.Model):
    name = models.CharField(max_length=150)
    price = models.PositiveIntegerField(null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_cart_item")
    product = models.ForeignKey(Products,on_delete=models.CASCADE, related_name="product_cart_item")

