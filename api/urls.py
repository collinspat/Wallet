from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.urls import path



schema_view = get_schema_view(
    openapi.Info(
        title="Sacco API",
        default_version='v1',
        description="API documentation for managing Assets ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.host"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)




# app_name = "api"
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('users/', include('users_management.urls')),
    path('saccos/', include('sacco_management.urls')),
    path('Assets/', include('asset_management.urls')),
    
    

]
