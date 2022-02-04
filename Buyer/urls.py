from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import refresh_jwt_token
router = DefaultRouter()
router.register(r'shipping-countries', views.ShippingCountriesAPI, basename='shipping-countries')
router.register(r'coupon', views.CouponAPI, basename='coupon')
router.register(r'address', views.BuyerAddressAPI, basename='Buyer-address')
router.register(r'order-tab', views.OrderTabAdminAPI, basename='Admin Order Tab')
urlpatterns = [
    path('', include(router.urls)),
    path('buyer/', views.BuyerAPI.as_view(), name='Buyer-API'),
    path('activate-deactivate/', views.ActivateDeactivateUserAPI.as_view(), name='Activate or Deactivate'),
    path('cart/', views.BuyerCartAPI.as_view(), name='Buyer Cart'),
    path('user-detail/', views.BuyerAndOrdersAPI.as_view(), name='User-Detail with Orders'),
    path('order-number-by-date/', views.OrderNumbersByDateAPI.as_view(), name='Filter Order on a Set Date'),
    path('order-number-by-category/', views.OrderNumbersByCategoryAPI.as_view(), name='Filter Order on a Set Category'),
    path('order-number-by-product/', views.OrderNumbersByProductAPI.as_view(), name='Filter Order on a Set Category'),
    path('search-user/', views.SearchUser.as_view(), name='Search-User'),
    path('order/', views.OrderAPI.as_view(), name='Buyer Order'),
    path('return/', views.ReturnProductAPI.as_view(), name='Return Product'),
    path('invoice-email/', views.SendEmailAPI.as_view(), name='Send E-mail')
]
