from django.db import models
from . import choices


# Brand Model
class Brand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    brandName = models.CharField(max_length=50, unique=True)
    brandImage = models.ImageField(upload_to='Brand/images')

    def __str__(self):
        return str(self.brandName)


# Category Model
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category_name = models.CharField(max_length=500, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')

    def __str__(self):
        return str(self.category_name)


# Size Model
class Size(models.Model):
    sizeID = models.AutoField(primary_key=True)
    size = models.CharField(max_length=50, unique=True)
    size_name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Main Product Model
class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    product_id = models.AutoField(primary_key=True)
    brandName = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=choices.Gender_Choices, default='ME')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=50)
    product_description = models.CharField(max_length=350, null=True)
    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    discount_type = models.CharField(max_length=2, choices=choices.Discount_Type, default='PE')
    product_discount = models.IntegerField(max_length=100, default=0)
    product_size = models.JSONField(null=True)
    product_material = models.CharField(max_length=2, choices=choices.Clothing_Material, default='NO')
    product_occasion = models.CharField(max_length=2, choices=choices.OCCASIONS, default='CA')
    product_color = models.JSONField(default=list)


# Product Variant with specific product and color
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.CharField(max_length=2, choices=choices.COLORS)
    quantity = models.IntegerField(max_length=500)


# Collections Model
class Collections(models.Model):
    collection_id = models.AutoField(primary_key=True)
    collection_title = models.CharField(max_length=500, unique=True)
    collection_desc = models.CharField(max_length=500)
    collection_image = models.ImageField(upload_to='Collections/images')
    created_at = models.DateTimeField(auto_now_add=True)


# Collection Variant including specific Product
class CollectionsVariant(models.Model):
    collection = models.ForeignKey(Collections, on_delete=models.CASCADE)
    product = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_imageID = models.AutoField(primary_key=True)
    product_image = models.ImageField(upload_to='products')
    product_color = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
