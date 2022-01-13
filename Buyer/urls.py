from django.urls import path
from .views import BuyerAPI
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('buyer/', BuyerAPI.as_view(), name='Buyer-API'),
]
