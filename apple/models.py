from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    image=models.FileField(blank=True)
    
    def __str__(self):
        return f'category:{self.name}'


class Product(models.Model):
    name=models.CharField(max_length=1000,unique=True)
    desc=models.TextField(max_length=10000)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    discount=models.IntegerField()
    image=models.FileField(default='default.jpg')
    catid=models.ForeignKey(Category,on_delete=CASCADE)
    stock=models.IntegerField()

    def __str__(self):
        return self.name



    def get_absolute_url(self):
            return reverse('apple:owner')
    


class Owner(models.Model):
    owner=models.CharField(max_length=1000)
    password=models.CharField(max_length=100)

    def __str__(self):
            return self.owner


