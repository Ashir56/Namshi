from rest_framework.serializers import ModelSerializer, SerializerMethodField, ChoiceField, JSONField
from rest_framework_recursive.fields import RecursiveField
from .models import Product, Brand, Category, Size,\
     ProductVariant, Collections,\
     CollectionsVariant
from rest_framework.exceptions import ValidationError
from . import choices
import json


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        lists = eval(data.get('product_color'))
        choices_list = []
        for choice in choices.COLORS:
            choices_list.append(choice[0])
        for list in lists:
            if list not in choices_list:
                raise ValidationError({'product_color': '{} is not a valid choice'.format(list)})

        return data


class ProductUpdateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


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


# class ColorSerializer(ModelSerializer):
#     class Meta:
#         model = Color
#         fields = '__all__'


class CollectionSerializer(ModelSerializer):
    # image along with the url
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


# class OccasionSerializer(ModelSerializer):
#     class Meta:
#         model = Occasion
#         fields = '__all__'
