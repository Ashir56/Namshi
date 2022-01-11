from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'brand', views.BrandAPI, basename='Brand')
router.register(r'product', views.ProductAPI, basename='Product')
router.register(r'category', views.CategoryAPI, basename='Product-Category')
router.register(r'sub-category', views.SubCategoryAPI, basename='Product-SubCategory')
router.register(r'size', views.SizeAPI, basename='Sizes')
router.register(r'category-sizes', views.CategorySizesAPI, basename='Category-Sizes')

urlpatterns = [
    path('', include(router.urls)),
    path('filter-by-brand/', views.FilterByBrand.as_view()),
    path('filter-by-category/', views.FilterByCategory.as_view()),
    path('sizes/', views.SizeTypeAPI.as_view(), name='Product-SizeType')
]
