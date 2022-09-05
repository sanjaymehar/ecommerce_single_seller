from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from apple.models import Product
# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)  
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
            return str(self.id)  

status_choice=(('Pending','Pending'),('Accepted','Accepted'),('Packed','Packed'),('On The Way','On The Way'),('Delivered','Delivered'),('Cancel','Cancel'),)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)  
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50,choices=status_choice,default='Pending')

    def __str__(self):
            return str(self.id)