from rest_framework.serializers import ModelSerializer
from .models import Product, Brand, Category, SubCategory


class ProductSerializer(ModelSerializer):
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
