from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from audit_trail.views import *


@swagger_auto_schema(
    method='post',
    operation_summary="Create a new Sacco",
    request_body=SaccoSerializer,
    responses={201: SaccoSerializer}
)
#sacco Crud
@api_view(['GET', 'POST'])

def SaccoLists(request):
    if request.method == 'GET':
        sacco = Sacco.objects.all()
        serializer = SaccoSerializer(sacco, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SaccoSerializer(data=request.data)
        if serializer.is_valid():
            sacco=serializer.save()         
                     
            create_audit_post_message(request,serializer,sacco)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='put',
    operation_summary="update a  Sacco",
    request_body=SaccoSerializer,
    responses={201: SaccoSerializer}
)    
@api_view(['GET', 'PUT', 'DELETE'])
def SaccoDetails(request, pk):
    try:
        sacco = Sacco.objects.get(pk=pk)
    except Sacco.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SaccoSerializer(sacco)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SaccoSerializer(sacco, data=request.data)
        if serializer.is_valid():           
            create_audit_edit_message(request,serializer,sacco)
            sacco=serializer.save()            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        create_audit_delete_message(request,sacco)
        sacco.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#sacco branches
@swagger_auto_schema(
    method='post',
    operation_summary="Create a new Sacco Branch",
    request_body=SaccoMemberSerializer,
    responses={201: SaccoMemberSerializer}
)
@api_view(['GET', 'POST'])
def SaccoBranchLists(request,id):
    sacco_branch = SaccoBranches.objects.filter(sacco_id=id)
    
    if request.method == 'GET':
        serializer = SaccoMemberSerializer(sacco_branch, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SaccoMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_audit_post_message(request,serializer,sacco_branch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    method='put',
    operation_summary="update a  Sacco Branch",
    request_body=SaccoMemberSerializer,
    responses={201: SaccoMemberSerializer}
)
@api_view(['GET', 'PUT', 'DELETE'])
def SaccoBranchDetails(request, pk):
    try:
        sacco_branch = SaccoBranches.objects.get(pk=pk)
    except SaccoBranches.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SaccoMemberSerializer(sacco_branch)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SaccoMemberSerializer(sacco_branch, data=request.data)
        if serializer.is_valid():
            create_audit_edit_message(request,serializer,sacco_branch)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        create_audit_delete_message(request,sacco_branch)
        sacco_branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)