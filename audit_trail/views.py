# Import necessary modules and classes from Django and Django REST Framework
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

# Function to add system logs
# This function creates a new entry in the ActivityLogs model with the provided details.
def add_system_logs(user, action, description, origin, ip_address, user_agent, x_forwarded_for):
    ActivityLogs.objects.create(
        user=user,
        action=action,
        description=description,
        origin=origin,
        ip_address=ip_address,
        user_agent=user_agent,
        x_forwarded_for=x_forwarded_for
    )

# Function to add new system logs based on the request
# This function creates a new log entry using details from the request object.
def add_new_system_logs(request, description, content_object):  
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get('HTTP_X_FORWARDED_FOR') else None
    
    ActivityLogs.objects.create(
        user=request.user,
        action=request.method,
        description=description,        
        content_object=content_object,
        ip_address=request.META['REMOTE_ADDR'],
        user_agent=request.META['HTTP_USER_AGENT'],        
        x_forwarded_for=x_forwarded_for
    )

# Function to get audit logs for a specific origin and ID
# You can use this to get logs for a specific user, sacco, or member.
def get_audit_logs(origin, id):
    member_type = ContentType.objects.get_for_model(origin)
    log = ActivityLogs.objects.filter(content_type=member_type, object_id=id)
    logs = ActivityLogsSerializer(log, many=True)
    return logs.data

# Function to create an audit message for edits
# This function logs changes made to an instance by comparing original and new values.
def create_audit_edit_message(request, serializer, instance):
    changes = []
    for field, new_value in serializer.validated_data.items():
        # Get the original value
        original_value = getattr(instance, field)
        if original_value != new_value:
            changes.append(f"{field} from {original_value} to {new_value}")
            
    if changes:
        change_count = len(changes)
        changes_description = '; '.join(changes)
        description = f"{change_count} change{'s' if change_count > 1 else ''}: {changes_description}."               
        add_new_system_logs(request, description, instance)

# Function to create an audit message for new entries
# This function logs the creation of a new instance with its field values.
def create_audit_post_message(request, serializer, instance):
    changes = []
    for field, new_value in serializer.validated_data.items():        
        changes.append(f"{field} : {new_value}")
        
    if changes:
        change_count = len(changes)
        changes_description = '; '.join(changes)
        description = f"New Entry : {changes_description}."
        
        add_new_system_logs(request, description, instance)

# Function to create an audit message for deletions
# This function logs the deletion of an instance.
def create_audit_delete_message(request, instance):
    description = f"Deleted Entry : {instance}."
    add_new_system_logs(request, description, instance)

# Function to create an audit message for approvals
# This function logs approved changes made to an instance.
def create_audit_approve_message(request, serializer, instance):
    changes = []
    for field, new_value in serializer.validated_data.items():
        # Get the original value
        original_value = getattr(instance, field)
        if original_value != new_value:
            changes.append(f"{field} from {original_value} to {new_value}")
            
    if changes:
        change_count = len(changes)
        changes_description = '; '.join(changes)
        description = f"{change_count} Approved change{'s' if change_count > 1 else ''}: {changes_description}."               
        add_new_system_logs(request, description, instance)