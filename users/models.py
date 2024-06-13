from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
        
class Address(models.Model):
    
    HOME = 'Home'
    WORK = 'Work'
    OTHER = 'Other'

    ADDRESS_TYPE_CHOICES = [
    (HOME, 'Home'),
    (WORK, 'Work'),
    (OTHER, 'Other'),
]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.IntegerField(max_length=6)
    country = models.CharField(max_length=50)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default=HOME)
    
    class Meta:
        verbose_name_plural = "Addresses"
        
    def __str__(self):
        return f"{self.get_address_type_display()}: {self.street}, {self.city}, {self.state}, {self.postal_code}"
