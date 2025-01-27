from .models import *
from rest_framework import serializers
from django.db.models import fields

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class UsersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = '__all__'
        
class LoginSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = ('email', 'password')
        
class TempSubPermissionsserializer(serializers.ModelSerializer):
    class Meta:
        model = TempSubPermissions
        fields = "__all__"
        
class TempPermissionsserializer(serializers.ModelSerializer):
    children = TempSubPermissionsserializer(many=True)

    class Meta:
        model = TempPermissions
        fields = "__all__"


class Permissionsserializer(serializers.ModelSerializer):
    class Meta:
        model = NewPermissions
        fields = "__all__"
