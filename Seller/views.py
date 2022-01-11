from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Brand, Category, SubCategory,\
    ProductQuantity, CategorySizes, Size
from .serializer import ProductSerializer, BrandSerializer, CategorySerializer,\
    SubCategorySerializer, ProductCreateSerializer, \
    SizeSerializer, CategorySizeSerializer, ProductQuantitySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
import json


TOP_SIZES = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']
BOTTOM_SIZES = [28, 30, 32, 34, 36, 38, 40, 42]
SHOE_INTL_SIZES = [40, 41, 42, 43, 44, 45, 46]
SHOE_US_SIZES = [6, 7, 8, 9, 10, 11, 12]
SHOE_UK_SIZES = [7, 8, 9, 10, 11, 12, 13]


class BrandAPI(ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [IsAdminUser, AllowAny, ]

    def get_serializer_class(self):
        return BrandSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


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
        request.data._mutable = True
        list = request.data.get('product_size')
        request.data['product_size'] = json.dumps(list)
        request.data._mutable = False
        return super(ProductAPI, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        list = instance.product_size
        list = eval(list)
        instance.product_size = list
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SizeTypeAPI(GenericAPIView):
    def get(self, request):
        try:
            size_type = request.data['sizeType']
            sizes = [TOP_SIZES, BOTTOM_SIZES]
            if size_type == 'IN':
                sizes.append(SHOE_INTL_SIZES)
            elif size_type == 'US':
                sizes.append(SHOE_US_SIZES)
            elif size_type == 'UK':
                sizes.append(SHOE_UK_SIZES)
            else:
                return Response({"success": False, "msg": "Not a valid size type"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"success": True, "sizes": str(sizes)},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryAPI(viewsets.ModelViewSet):

    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


class SubCategoryAPI(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()

    def get_serializer_class(self):
        return SubCategorySerializer

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

            return Response({"success": True, "brands": ser}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Something went wrong"}, status=status.
                            HTTP_500_INTERNAL_SERVER_ERROR)


class SizeAPI(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]


class CategorySizesAPI(viewsets.ModelViewSet):
    queryset = CategorySizes.objects.all()
    serializer_class = CategorySizeSerializer
    permission_classes = [IsAdminUser, ]