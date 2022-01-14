from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('buyer/', views.BuyerAPI.as_view(), name='Buyer-API'),
    path('activate-deactivate/', views.ActivateDeactivateAPI.as_view(), name='Activate or Deactivate'),
    path('search-user/', views.SearchUser.as_view(), name='Search-User')
]
