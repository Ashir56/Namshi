from django.db import models


class Brand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    brandName = models.CharField(max_length=50, unique=True)
    brandImage = models.ImageField(upload_to='Brand/images')

    def __str__(self):
        return str(self.brandName)


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.category)


class SubCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sub_category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.sub_category)


class Product(models.Model):
    Gender_Choices = [
        ('ME', 'Men'),
        ('WO', 'Women'),
        ('KI', 'Kid'),
        ('BE', 'Beauty')
    ]

    SIZETYPE_CHOICES = [
        ('US', 'USA'),
        ('UK', 'UKingdom'),
        ('IN', 'International')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    product_id = models.AutoField(primary_key=True)
    brandName = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=Gender_Choices, default='ME')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=50)
    product_description = models.CharField(max_length=350, null=True)
    product_price = models.IntegerField(max_length=100)
    product_discount = models.IntegerField(max_length=100)
    product_sizeType = models.CharField(max_length=2, choices=SIZETYPE_CHOICES, default='IN')
    product_size = models.CharField(max_length=2)
    product_color = models.CharField(max_length=50)
    product_image1 = models.ImageField(null=True, upload_to='Product/images')
    product_image2 = models.ImageField(null=True, upload_to='Product/images')
    product_image3 = models.ImageField(null=True, upload_to='Product/images')
    product_image4 = models.ImageField(null=True, upload_to='Product/images')
    product_image5 = models.ImageField(null=True, upload_to='Product/images')
    product_imageList = models.JSONField(null=True)
