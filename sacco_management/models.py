from django.db import models
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog


# Create your models here.

class Sacco(models.Model):
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    logo = models.CharField(max_length=100, null=True, blank=True)
    profile = models.ForeignKey('user_management.Profile', on_delete=models.SET_NULL, null=True, blank=True,related_name='sacco_profiles_list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    

    
    
class SaccoBranches(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True,blank=True, related_name='branches')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


auditlog.register(Sacco)
auditlog.register(SaccoBranches)