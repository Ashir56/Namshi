from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Brand, Category,\
    ProductVariant, Size, Color,\
    Collections, ProductCollections
from .serializer import ProductSerializer, BrandSerializer, CategorySerializer,\
    ProductCreateSerializer, SizeSerializer,\
    ProductVariantSerializer, ColorSerializer,\
    CollectionSerializer, ProductCollectionsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db import transaction
import json


class BrandAPI(ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [IsAdminUser, AllowAny, ]

    def get_serializer_class(self):
        return BrandSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAdminUser, ]
        return super(BrandAPI, self).get_permissions()


class ProductAPI(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser, AllowAny, ]

    def get_serializer_class(self):
        if self.action in 'create':
            self.serializer_class = ProductCreateSerializer
        else:
            self.serializer_class = ProductSerializer
        return super(ProductAPI, self).get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            request.data._mutable = True
            product_list = request.data.get('product_size')
            request.data['product_size'] = json.dumps(product_list)
            serializer = ProductCreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            product = serializer.instance
            product_sizes = eval(product.product_size)
            sizes = []
            quantities = eval(request.data['product_quantity'])
            for product_size in product_sizes:
                size = Size.objects.get(size=product_size)
                sizes.append(size)
            color_id = request.data.get('product_color')
            color = Color.objects.get(color_id=color_id)
            i = 0
            # add sizes and colors along with their quantities
            while i < len(sizes):
                ProductVariant.objects.create(product=product, size=sizes[i], quantity=quantities[i], color=color)
                i += 1
            request.data._mutable = False
            return Response({"success": True, "msg": "Product Created"}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        size = instance.product_size
        product_list = eval(size)
        instance.product_size = product_list
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
        return super().get_permissions()


class FilterByBrand(GenericAPIView):
    def post(self, request):
        try:
            gender = request.data.get('gender')
            products = Product.objects.filter(gender=gender)
            brands = []
            ser = []
            for product in products:
                brand = product.brandName
                if not brand in brands:
                    brands.append(brand)
                    serializer = BrandSerializer(brand)
                    ser.append(serializer.data)

            return Response({"success": True, "brands": ser}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Something went wrong"}, status=status.
                            HTTP_500_INTERNAL_SERVER_ERROR)


class FilterByCategory(GenericAPIView):
    def post(self, request):
        try:
            gender = request.data.get('gender')
            products = Product.objects.filter(gender=gender)
            categories = []
            ser = []
            for product in products:
                category = product.product_category
                if not category in categories:
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
    permission_classes = [IsAdminUser, ]


class ColorAPI(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]


class CollectionAPI(viewsets.ModelViewSet):
    queryset = Collections.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        permission_classes = [IsAdminUser]
        return super(CollectionAPI, self).get_permissions()


class ProductCollectionsAPI(viewsets.ModelViewSet):
    queryset = ProductCollections.objects.all()
    serializer_class = ProductCollectionsSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny, ]
        permission_classes = [IsAdminUser, ]
        return super(ProductCollectionsAPI, self).get_permissions()

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
        product_collection = ProductCollections.object.get(collection=collection)
        product_ids = eval(product_collection.product)
        for product_id in product_ids:
            product = Product.objects.get(product_id=product_id)
            if product:
                serializer = ProductSerializer(product, many=True)
                ser.append(serializer.data)
        return Response(ser, status=status.HTTP_200_OK)
