from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import Product, Brand, Category,\
    ProductVariant, Size,\
    Collections, CollectionsVariant
from .serializer import BrandSerializer, CategorySerializer,\
    ProductSerializer, SizeSerializer,\
    ProductVariantSerializer, CollectionSerializer, ProductCollectionsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db import transaction
import json


# add/edit/delete a brand
# create a new brand
class BrandAPI(ModelViewSet):
    queryset = Brand.objects.all()
    # permission_classes = [IsAdminUser, AllowAny, ]

    def get_serializer_class(self):
        return BrandSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(BrandAPI, self).get_permissions()


# add/edit/delete a product
class ProductAPI(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # view all the products and open details of a product
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(ProductAPI, self).get_permissions()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            request.data._mutable = True
            request.data['product_color'] = json.dumps(request.data.get('product_color'))
            size = request.data.get('product_size')
            request.data['product_size'] = json.dumps(size)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            product = serializer.instance
            product_colors = eval(product.product_color)
            product_sizes = eval(product.product_size)
            product_quantities = eval(request.data.get('product_quantity'))
            quantities = 0
            color_counter = 0
            length = 0
            for product_size in product_sizes:
                for value in product_size:
                    length += 1
            if len(product_quantities) != length:
                return Response({'success': False, 'product': 'size and quantity does not have the same length'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            for product_size in product_sizes:
                i = 0
                sizes = []
                for value in product_size:
                    size = Size.objects.get(size=value)
                    sizes.append(size)
                while i < len(sizes):
                    ProductVariant.objects.create(product=product, size=sizes[i],
                                                  quantity=product_quantities[quantities],
                                                  color=product_colors[color_counter]
                                                  )
                    i += 1
                    quantities += 1
                color_counter += 1
            request.data._mutable = False
            return Response({"success": True, "msg": "Product Created"}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        size = instance.product_size
        product_list = eval(size)
        instance.product_size = product_list
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# add/edit/delete a category
# create a new category
class CategoryAPI(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Category.objects.filter(parent__isnull=True)
        return Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(CategoryAPI, self).get_permissions()


# Filter By Category
class FilterByCategory(GenericAPIView):
    def post(self, request):
        try:
            category_id = request.data.get('category')
            category = Category.objects.get(category_id=category_id)
            products = Product.objects.filter(product_category=category)
            ser = []
            for product in products:
                serializer = ProductSerializer(product)
                ser.append(serializer.data)
            return Response(ser, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Filter by Brand
class FilterByBrand(GenericAPIView):
    def post(self, request):
        try:
            brand_id = request.data.get('brand')
            brand = Brand.objects.get(id=brand_id)
            products = Product.objects.filter(brandName=brand)
            ser = []
            for product in products:
                serializer = ProductSerializer(product)
                ser.append(serializer.data)
            return Response(ser, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Filter by Brand and Category
class FilterByBrandAndCategory(GenericAPIView):
    def post(self, request):
        try:
            category_id = request.data.get('category')
            category = Category.objects.get(category_id=category_id)
            brand_id = request.data.get('brand')
            brand = Brand.objects.get(id=brand_id)
            products = Product.objects.filter(brandName=brand, product_category=category)
            ser = []
            for product in products:
                serializer = ProductSerializer(product)
                ser.append(serializer.data)
            return Response(ser, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterByGender(GenericAPIView):
    def post(self, request):
        try:
            gender = request.data.get('gender')
            products = Product.objects.filter(gender=gender)
            brands = []
            ser = []
            for product in products:
                brand = product.brandName
                if brand not in brands:
                    brands.append(brand)
                    serializer = BrandSerializer(brand)
                    ser.append(serializer.data)

            return Response({"success": True, "brands": ser}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Something went wrong"}, status=status.
                            HTTP_500_INTERNAL_SERVER_ERROR)


class FilterByGenderCategory(GenericAPIView):
    def post(self, request):
        try:
            gender = request.data.get('gender')
            products = Product.objects.filter(gender=gender)
            categories = []
            ser = []
            for product in products:
                category = product.product_category
                if category not in categories:
                    categories.append(category)
                    serializer = CategorySerializer(category)
                    ser.append(serializer.data)

            return Response({"success": True, "brands": ser},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SizeAPI(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(SizeAPI, self).get_permissions()


# class ColorAPI(viewsets.ModelViewSet):
#     queryset = Color.objects.all()
#     serializer_class = ColorSerializer
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             self.permission_classes = [AllowAny]
#         else:
#             self.permission_classes = [IsAdminUser]
#         return super(ColorAPI, self).get_permissions()


#  add/edit/delete collection
class CollectionAPI(viewsets.ModelViewSet):
    queryset = Collections.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(CollectionAPI, self).get_permissions()


class CollectionsVariantAPI(viewsets.ModelViewSet):
    queryset = CollectionsVariant.objects.all()
    serializer_class = ProductCollectionsSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(CollectionsVariantAPI, self).get_permissions()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            request.data._mutable = True
            product_list = request.data.get('product_list')
            request.data['product_size'] = json.dumps(product_list)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            request.data._mutable = False
            return Response({"success": True, "msg": "Product Created"}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        collection_id = request.data.get('collection_id')
        collection = Collections.object.get(collection_id=collection_id)
        ser = []
        product_collection = CollectionsVariant.object.get(collection=collection)
        product_ids = eval(product_collection.product)
        for product_id in product_ids:
            product = Product.objects.get(product_id=product_id)
            if product:
                serializer = ProductSerializer(product, many=True)
                ser.append(serializer.data)
        return Response(ser, status=status.HTTP_200_OK)


class DiscountAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            discount = request.data.get('discount')
            discount_type = request.data.get('discount_type')
            product_id = request.GET.get('product_id')
            product = Product.objects.get(product_id=product_id)
            product.product_discount = discount
            product.discount_type = discount_type
            product.save()
            return Response({"success": True, "msg": "Discount Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            product_id = request.GET.get('product_id')
            product = Product.objects.get(product_id=product_id)
            product.product_discount = 0
            product.save()
            return Response({"success": True, "msg": "Discount Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            discount_type = request.data.get('discount_type')
            products = Product.objects.filter(discount_type=discount_type)
            ser = []
            for product in products:
                serializer = ProductSerializer(product, many=True)
                ser.append(serializer.data)
            return Response(ser, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class OccasionAPI(ModelViewSet):
#     queryset = Occasion.objects.all()
#     serializer_class = OccasionSerializer
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             self.permission_classes = [AllowAny, ]
#         else:
#             self.permission_classes = [IsAdminUser, ]
#         return super(OccasionAPI, self).get_permissions()

