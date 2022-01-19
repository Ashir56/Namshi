from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import refresh_jwt_token
router = DefaultRouter()
router.register(r'shipping-countries', views.ShippingCountriesAPI, basename='shipping-countries')
router.register(r'coupon', views.CouponAPI, basename='coupon')
urlpatterns = [
    path('', include(router.urls)),
    path('buyer/', views.BuyerAPI.as_view(), name='Buyer-API'),
    path('activate-deactivate/', views.ActivateDeactivateAPI.as_view(), name='Activate or Deactivate'),
    path('search-user/', views.SearchUser.as_view(), name='Search-User')
]
