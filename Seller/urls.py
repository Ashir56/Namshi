from django.urls import path, include
from .views import ProductAPI, ShopAPI, SizeTypeAPI, FilterByBrand,\
    CategoryAPI, SubCategoryAPI
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'shop-api', ShopAPI, basename='Brand')
router.register(r'product', ProductAPI, basename='Product')
router.register(r'category', CategoryAPI, basename='Product-Category')
router.register(r'sub-category', SubCategoryAPI, basename='Product-SubCategory')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('filterbybrand/', FilterByBrand.as_view()),
    path('sizes/', SizeTypeAPI.as_view(), name='Product-SizeType')
]
