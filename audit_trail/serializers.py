from .models import *
from rest_framework import serializers
from django.db.models import fields

class ActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLogs
        fields = '__all__'