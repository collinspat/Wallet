from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .functions import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import authentication_classes, permission_classes
from audit_trail.views import *
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from audit_trail.views import *
from reports.functions import *
from reports.models import *
from datetime import date
from rest_framework import viewsets

@swagger_auto_schema(
    method='post',
    request_body=AssetSerializer,
    operation_summary='Register a new asset',
    responses={200: AssetSerializer}
    )
    
#crud for asset
@api_view(['GET', 'POST'])
def asset_list(request):
    if request.method == 'GET':
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def asset_detail(request, pk):
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AssetSerializer(asset)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_edit_message(request, serializer, asset)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        create_audit_delete_message(request, asset)
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#crud for appreciation
@swagger_auto_schema(
    method='post',
    request_body=AppreciationSerializer,
    operation_summary='Register a new appreciation',
    responses={200: AppreciationSerializer}
    )
@api_view(['GET', 'POST'])
def appreciation_list(request):
    if request.method == 'GET':
        appreciations = Appreciation.objects.all()
        serializer = AppreciationSerializer(appreciations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AppreciationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def appreciation_detail(request, pk):
    try:
        appreciation = Appreciation.objects.get(pk=pk)
    except Appreciation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AppreciationSerializer(appreciation)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AppreciationSerializer(appreciation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_edit_message(request, serializer, appreciation)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        create_audit_delete_message(request, appreciation)
        appreciation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
  

    

#crud for depreciation
@swagger_auto_schema(
    method='post',
    request_body=DepreciationSerializer,
    operation_summary='depreciation of an asset',
    responses={200: DepreciationSerializer}
    )
@api_view(['GET', 'POST'])
def depreciation_list(request):
    if request.method == 'GET':
        depreciations = Depreciation.objects.all()
        serializer = DepreciationSerializer(depreciations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepreciationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def depreciation_detail(request, pk):
    try:
        depreciation = Depreciation.objects.get(pk=pk)
    except Depreciation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DepreciationSerializer(depreciation)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DepreciationSerializer(depreciation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_edit_message(request, serializer, depreciation)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        create_audit_delete_message(request, depreciation)
        depreciation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


#crud for maintainance 
@swagger_auto_schema(
    method='post',
    request_body=MaintenanceSerializer,
    operation_summary='maintainance of an asset',
    responses={200: MaintenanceSerializer}
    )
@api_view(['GET', 'POST'])
def maintenance_list(request):
    if request.method == 'GET':
        maintenance = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#crud for lifecycle
@swagger_auto_schema(
    method='post',
    request_body=LifecycleSerializer,
    operation_summary='lifecycle of an asset',
    responses={200: LifecycleSerializer}
    )
@api_view(['GET', 'POST'])
def lifecycle_list(request):
    if request.method == 'GET':
        lifecycle = Lifecycle.objects.all()
        serializer = LifecycleSerializer(lifecycle, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LifecycleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',  'DELETE'])
def lifecycle_detail(request, pk):
    try:
        lifecycle = Lifecycle.objects.get(pk=pk)
    except Lifecycle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LifecycleSerializer(lifecycle)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        create_audit_delete_message(request, lifecycle)
        lifecycle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#crud for maintenance
@swagger_auto_schema(
    method='post',
    request_body=MaintenanceSerializer,
    operation_summary='maintenance of an asset',
    responses={200: MaintenanceSerializer}
    )
@api_view(['GET', 'POST'])
def maintenance_list(request):
    if request.method == 'GET':
        maintenance = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def maintenance_detail(request, pk):
    try:
        maintenance = Maintenance.objects.get(pk=pk)
    except Maintenance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MaintenanceSerializer(maintenance)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MaintenanceSerializer(maintenance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_edit_message(request, serializer, maintenance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        create_audit_delete_message(request, maintenance)
        maintenance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




 #crud for risk
@swagger_auto_schema(
    method='post',
    request_body=RiskSerializer,
    operation_summary='risk of an asset',
    responses={200: RiskSerializer}
    )
@api_view(['GET', 'POST'])
def risk_list(request):
    if request.method == 'GET':
        risk = Risk.objects.all()
        serializer = RiskSerializer(risk, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RiskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def risk_detail(request, pk):
    try:
        risk = Risk.objects.get(pk=pk)
    except Risk.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RiskSerializer(risk)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RiskSerializer(risk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_edit_message(request, serializer, risk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        create_audit_delete_message(request, risk)
        risk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    