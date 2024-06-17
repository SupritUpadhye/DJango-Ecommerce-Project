from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobNo = models.CharField(max_length=15, blank=True)  
    profile_img = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg')  
    
    def __str__(self):
        return self.username

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('guardian', 'Guardian'),
    )
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)  
    pincode = models.CharField(max_length=10)  
    mobile_number = models.CharField(max_length=15)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    
    def __str__(self):
        return f"{self.address_type} Address for {self.user.username}"


