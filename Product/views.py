from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Brand, Category,\
    ProductVariant, Size,\
    Collections, CollectionsVariant, ProductImage
from .serializer import BrandSerializer, CategorySerializer,\
    ProductSerializer, SizeSerializer, ProductImageSerializer,\
    ProductVariantSerializer, CollectionSerializer, ProductCollectionsSerializer, ProductCreateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json


# add/edit/delete a brand
# create a new brand
class BrandAPI(ModelViewSet):
    queryset = Brand.objects.all()

    def get_serializer_class(self):
        return BrandSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [AllowAny, ]
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

    # Creating Product
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            request.data._mutable = True
            # Changing lists into json serialized
            request.data['product_color'] = json.dumps(request.data.get('product_color'))
            request.data['product_size'] = json.dumps(request.data.get('product_size'))
            # Creating Product using serializer
            serializer = ProductCreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            product = serializer.instance
            product_colors = eval(product.product_color)
            product_sizes = eval(product.product_size)
            product_quantities = eval(request.data.get('product_quantity'))
            product_images = eval(request.data.get('product_image'))
            quantities_counter = 0
            color_counter = 0
            length = 0
            image_length = 0
            # getting quantities of sizes and images
            for product_size in product_sizes:
                for value in product_size:
                    length += 1
            for product_image in product_images:
                image_length += 1
            # Checking if quantities of product and sizes are same
            if len(product_quantities) == length and len(product_colors) == image_length\
                    and len(product_colors) == len(product_sizes):
                # Creating instance of Product image containing list of images for particular color
                for product_image in product_images:
                    images = []
                    for value in product_image:
                        images.append(value)
                    ProductImage.objects.create(product_id=product, product_images=str(images),
                                                product_color=product_colors[color_counter])
                    color_counter += 1
                color_counter = 0
                # Creating variants for Product
                for product_size in product_sizes:
                    i = 0
                    sizes = []
                    for value in product_size:
                        size = Size.objects.get(size=value)
                        sizes.append(size)
                    while i < len(sizes):
                        ProductVariant.objects.create(product=product, size=sizes[i],
                                                      quantity=product_quantities[quantities_counter],
                                                      color=product_colors[color_counter]
                                                      )
                        i += 1
                        quantities_counter += 1
                    color_counter += 1
                request.data._mutable = False
                return Response({"success": True, "msg": "Product Created"}, status=status.HTTP_200_OK)
            else:
                # Roll back Transition if any exceptions occur
                raise transaction.rollback()

    # Get Product with images according to color
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        size = instance.product_size
        product_list = eval(size)
        instance.product_size = product_list
        ser = []
        serializer = self.get_serializer(instance)
        ser.append(serializer.data)
        # Retrieving images for that particular product
        products = ProductImage.objects.filter(product_id=instance.product_id)
        if products:
            for product in products:
                # Appending serializer list along with images
                serializer = ProductImageSerializer(product)
                ser.append(serializer.data)
        return Response(ser)

    # Deleting an instance along with its variant and images
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Retrieving Variants of that product
        variants = ProductVariant.objects.filter(product=instance)
        if variants:
            # Deleting the variants
            variants.delete()
        # Retrieving Images of thar Product
        images = ProductImage.objects.filter(product_id=instance)
        if images:
            # Deleting the images of product
            images.delete()
        # Deleting the product
        return super().destroy(request, *args, **kwargs)


# add/edit/delete a category
class CategoryAPI(viewsets.ModelViewSet):
    # Add Category
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
            # get Category
            category_id = request.data.get('category')
            category = Category.objects.get(category_id=category_id)
            products = Product.objects.filter(product_category=category)
            ser = []
            # Product Loops
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


# Filtering Products According to Gender
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
                # Check If Category Exists
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


# Adding/ Updating/ Deleting Sizes
class SizeAPI(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(SizeAPI, self).get_permissions()


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


# Adding/ Updating/ Deleting Collection Variants
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
            product_list = eval(request.data.get('product'))
            for product_id in product_list:
                try:
                    product = Product.objects.get(product_id=product_id)
                except ObjectDoesNotExist:
                    return Response({"success": False, str(product_id): "Product Does Not Exist"},
                                    status=status.HTTP_404_NOT_FOUND)
            request.data['product'] = json.dumps(product_list)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            request.data._mutable = False
            return Response({"success": True, "msg": "Product Created"}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        collection_id = request.GET.get('collection_id')
        collection = Collections.objects.get(collection_id=collection_id)
        ser = []
        product_collection = CollectionsVariant.objects.get(collection=collection)
        product_ids = eval(product_collection.product)
        for product_id in product_ids:
            product = Product.objects.get(product_id=product_id)
            if product:
                serializer = ProductSerializer(product, many=True)
                ser.append(serializer.data)
        return Response(ser, status=status.HTTP_200_OK)


# Adding Discounts in Product
class DiscountAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    # Adding Discounts in Products
    def post(self, request):
        try:
            discount = request.data.get('discount')
            discount_type = request.data.get('discount_type')
            product_id = request.GET.get('product')
            product = Product.objects.get(product_id=product_id)
            product.product_discount = discount
            product.discount_type = discount_type
            product.save()
            return Response({"success": True, "msg": "Discount Added"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Deleting Discounts of Product
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

    # Retrieving Discounts on Product
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


# Product Images According to color , size
class ProductImageAPI(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(ProductImageAPI, self).get_permissions()


# Adding/ Updating/ Deleting Product Variants
class ProductVariantAPI(ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(ProductVariantAPI, self).get_permissions()
