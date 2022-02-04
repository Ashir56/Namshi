import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from Product.models import Product, Size, ProductVariant
from . import choices
# Create your models here.


class Buyer(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    profile_pic = models.ImageField(null=True, upload_to='buyer')
    gender = models.CharField(max_length=10, blank=False)
    dob = models.DateField(max_length=10, null=True)
    phoneNumber = models.CharField(max_length=50, null=True)


class BuyerCard(models.Model):
    buyerCard_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    card_number = models.IntegerField(max_length=100)
    card_name = models.CharField(max_length=500)
    expiry_date = models.DateField()
    cvc_num = models.IntegerField(max_length=100)
    token = models.CharField(max_length=500)


class BuyerAddress(models.Model):
    buyerAddress_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    address = models.TextField(max_length=500)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_number = models.IntegerField(max_length=50)
    house_number = models.IntegerField(max_length=50)
    postal_code = models.IntegerField(max_length=50)
    address_type = models.CharField(max_length=2, choices=choices.Address_Type, default='HO')


class BuyerCart(models.Model):
    buyerCart_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(max_length=50, default=1)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)


class BuyerWishlist(models.Model):
    buyerWishlist_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)


class ShippingCountries(models.Model):
    shippingCountry_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=50)
    shipping_cost = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)


class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(ShippingCountries, on_delete=models.CASCADE, unique=True)
    coupon = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    coupon_type = models.CharField(max_length=2, choices=choices.Coupon_Type, default='PE')


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.JSONField(default=list)
    colors = models.JSONField(default=list)
    sizes = models.JSONField(default=list)
    prices = models.JSONField(default=list)
    quantities = models.JSONField(default=list)
    shipping_cost = models.FloatField(max_length=500, default=0.00)
    sub_total = models.FloatField(max_length=500,)
    grand_total = models.FloatField(max_length=500,)
    coupon = models.FloatField(max_length=500)
    order_status = models.PositiveIntegerField(max_length=2, choices=choices.Order_Type, default=1)


class ReturnProduct(models.Model):
    return_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    variant = models.ForeignKey(ProductVariant, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(max_length=500)
    price = models.BigIntegerField(max_length=500)
    buyer = models.ForeignKey(Buyer, on_delete=models.DO_NOTHING)


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    invoice = models.FileField(upload_to='invoice', null=True)