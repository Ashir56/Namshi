import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from Seller.models import Product
# Create your models here.


class Buyer(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    profile_pic = models.ImageField(null=True, upload_to='Buyer/Images')
    gender = models.CharField(max_length=10, blank=False)
    dob = models.DateField(max_length=10, null=True)
    phoneNumber = models.CharField(max_length=50, null=True)


class BuyerCard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    card_number = models.IntegerField(max_length=100)
    card_name = models.CharField(max_length=500)
    expiry_date = models.DateField()
    cvc_num = models.IntegerField(max_length=100)
    token = models.CharField(max_length=500)


class BuyerAddress(models.Model):

    Address_Type = [
        ('HO', 'House'),
        ('OF', 'Office')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    address = models.TextField(max_length=500)
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_number = models.IntegerField(max_length=50)
    home_number = models.IntegerField(max_length=50)
    postal_code = models.IntegerField(max_length=50)
    address_type = models.CharField(max_length=2, choices=Address_Type)


class BuyerCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)


class BuyerWishlist(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
