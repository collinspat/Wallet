from .views import *
from rest_framework import routers
from django.urls import path, include

urlpatterns = [
   
    path('asset/', asset_list),
    path('asset/<int:pk>/', asset_detail),

    

    path('depreciation/', depreciation_list),
    path('depreciation/<int:pk>/', depreciation_detail),

    path('lifecycle/', lifecycle_list),
    path('lifecycle/<int:pk>/', lifecycle_detail),

    path('maintenance/', maintenance_list),
    path('maintenance/<int:pk>/', maintenance_detail),

    path('risk/', risk_list),
    path('risk/<int:pk>/', risk_detail),
    ]


  
    