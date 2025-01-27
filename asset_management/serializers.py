from rest_framework import serializers
from .models import *

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class LifecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifecycle
        fields = '__all__'

class DepreciationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depreciation
        fields = '__all__'

class AppreciationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appreciation
        fields = '__all__'




class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'