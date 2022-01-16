from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from .models import Product, Brand, Category, Size,\
     ProductVariant, Color, Collections, CollectionsVariant, ShippingCountries
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
        jsonDec = json.decoder.JSONDecode()
        list = data.get('product_size')
        data['product_size'] = jsonDec.decode(list)
        return data


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(ModelSerializer):

    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['category_id', 'category_name', 'parent', 'children', ]


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductVariantSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CollectionSerializer(ModelSerializer):
    image_url = SerializerMethodField('get_image_url')

    class Meta:
        model = Collections
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.collection_image.url


class ProductCollectionsSerializer(ModelSerializer):
    class Meta:
        model = CollectionsVariant
        fields = '__all__'


class ShippingCountriesSerializer(ModelSerializer):
    class Meta:
        model = ShippingCountries
        fields = '__all__'