from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [   
    # profile
    path('profiles', GlobalProfileLists), 
    path('profiles/<int:id>', ProfileLists),
    path('profile/<int:pk>', ProfileDetails),
    
    # user registration
    path('users/<int:id>', UsersList, name='register'),
    path('user/<int:pk>', UserDetails, name='user'),
    
    path('login', login_view, name='clientlogin'),
    path('verify-otp', verify_otp, name='create_user'),
    path('reset-password', reset_password, name='create_user'),
    path ('forgot-password', forgot_password, name='create_user'),
    
    path("actions/<int:id>", actions_get_view, name="actions_get_view"),
    path("sacco/actions/<int:id>", sacco_actions_get_view, name="actions_get_view"),
    path("permissions/add", permissions_add_view, name="permissions_add"),
    path("permissions/get/<int:id>", permissions_get_view, name="permissions_get"),
    # Refresh token endpoint (for getting a new access token)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]