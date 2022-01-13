from django.db import models


class Brand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    brandName = models.CharField(max_length=50, unique=True)
    brandImage = models.ImageField(upload_to='Brand/images')

    def __str__(self):
        return str(self.brandName)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category_name = models.CharField(max_length=500, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')

    def __str__(self):
        return str(self.category_name)


class Size(models.Model):
    sizeID = models.AutoField(primary_key=True)
    size = models.CharField(max_length=50, unique=True)
    size_name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=50)


class Product(models.Model):
    Gender_Choices = [
        ('ME', 'Men'),
        ('WO', 'Women'),
        ('KI', 'Kid'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    product_id = models.AutoField(primary_key=True)
    brandName = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=Gender_Choices, default='ME')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=50)
    product_description = models.CharField(max_length=350, null=True)
    product_price = models.IntegerField(max_length=100)
    product_discount = models.IntegerField(max_length=100, default=0)
    product_size = models.JSONField(null=True)
    product_discountprice = models.IntegerField(max_length=50, default=0)
    product_color = models.ForeignKey(Color, on_delete=models.CASCADE)
    product_image1 = models.ImageField(null=True, upload_to='Product/images')
    product_image2 = models.ImageField(null=True, upload_to='Product/images')
    product_image3 = models.ImageField(null=True, upload_to='Product/images')
    product_image4 = models.ImageField(null=True, upload_to='Product/images')
    product_image5 = models.ImageField(null=True, upload_to='Product/images')
    product_imageList = models.JSONField(null=True)


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=500)


class Collections(models.Model):
    collection_id = models.AutoField(primary_key=True)
    collection_title = models.CharField(max_length=500, unique=True)
    collection_desc = models.CharField(max_length=500)
    collection_image = models.ImageField(upload_to='Collections/images')
    created_at = models.DateTimeField(auto_now_add=True)


class ProductCollections(models.Model):
    collection = models.ForeignKey(Collections, on_delete=models.CASCADE)
    product = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
