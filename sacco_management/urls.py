from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [    
    
   path('saccos', SaccoLists),
   path('saccos/<int:pk>', SaccoDetails),
   
   path('sacco_branches/<int:id>', SaccoBranchLists),
    path('sacco_branch/<int:pk>', SaccoBranchDetails),
]