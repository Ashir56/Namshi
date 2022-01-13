from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'brand', views.BrandAPI, basename='Brand')
router.register(r'product', views.ProductAPI, basename='Product')
router.register(r'category', views.CategoryAPI, basename='Product-Category')
router.register(r'size', views.SizeAPI, basename='Sizes')
router.register(r'color', views.ColorAPI, basename='Colors')
router.register(r'collection', views.CollectionAPI, basename='Collection')
router.register(r'product-collection', views.ProductCollectionsAPI, basename='Product-Collection')

urlpatterns = [
    path('', include(router.urls)),
    path('filter-by-brand/', views.FilterByBrand.as_view()),
    path('filter-by-category/', views.FilterByCategory.as_view()),
]
