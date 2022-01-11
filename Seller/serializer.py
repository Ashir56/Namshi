from rest_framework.serializers import ModelSerializer
from .models import Product, Brand, Category, SubCategory, Size, CategorySizes, ProductQuantity
import json


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        img1 = data.get('product_image1')
        img2 = data.get('product_image2')
        img3 = data.get('product_image3')
        img4 = data.get('product_image4')
        img5 = data.get('product_image5')

        images = [str(img1), str(img2), str(img3), str(img4), str(img5)]
        data['product_imageList'] = images

        return data


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        print("HELLO")
        jsonDec = json.decoder.JSONDecode()
        list = data.get('product_size')
        data['product_size'] = jsonDec.decode(list)
        return data


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class CategorySizeSerializer(ModelSerializer):
    class Meta:
        model = CategorySizes
        fields = '__all__'


class ProductQuantitySerializer(ModelSerializer):
    class Meta:
        model = ProductQuantity
        fields = '__all__'
