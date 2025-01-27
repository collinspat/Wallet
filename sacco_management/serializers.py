from .models import *
from .serializers import *
from rest_framework import serializers
from django.db.models import fields
 
class SaccoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sacco
        fields = '__all__'
        
class SaccoMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaccoBranches
        fields = '__all__'

