from rest_framework.serializers import ModelSerializer, SerializerMethodField, ChoiceField, JSONField
from rest_framework_recursive.fields import RecursiveField
from .models import Product, Brand, Category, Size,\
     ProductVariant, Collections,\
     CollectionsVariant, ProductImage
from rest_framework.exceptions import ValidationError
from . import choices


class ProductCreateSerializer(ModelSerializer):
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


class ProductSerializer(ModelSerializer):
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


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def validate(self, data):
        product_color = data.get('product_color')
        product = data.get('product_id')
        colorList = eval(product.product_color)
        if product_color not in colorList:
            raise ValidationError({'product_color': 'Input is not in valid product_colors'})

        return data
