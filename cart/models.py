from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from home.models import Product

# Create your models here.

class CartItem(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.title}'
    
    
