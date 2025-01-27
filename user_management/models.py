from django.db import models
from sacco_management.models import *
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500,null=True, blank=True) 
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True, blank=True,related_name='sacco_profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
auditlog.register(Profile)
    
    
class UsersModel(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=13)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=255)    
    address = models.CharField(max_length=255, blank=True, null=True)    
    first_login=models.BooleanField(default=True)
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE)   
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)    
    status = models.BooleanField(default=True)
    otp = models.CharField(max_length=10, blank=True, null=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.email
    
auditlog.register(Profile)

class Actions(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True, blank=True)
    deactivate = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=255, blank=True, null=True)
    custom_field = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class TempPermissions(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    action = models.ForeignKey(Actions, on_delete=models.SET_NULL, null=True)
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    deactivate = models.BooleanField(default=False)
    status = models.CharField(max_length=255)
    parent = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sacco} - {self.profile} - {self.action}"


class NewPermissions(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    action = models.ForeignKey(Actions, on_delete=models.SET_NULL, null=True)
    create = models.BooleanField(default=False)
    deactivate = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    status = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    # actioned_by = models.ForeignKey(
    #     UsersModel, on_delete=models.SET_NULL, blank=True, null=True
    # )

    def __str__(self):
        return f"{self.sacco} - {self.profile} - {self.action}"


class TempSubPermissions(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    action = models.ForeignKey(Actions, on_delete=models.SET_NULL, null=True)
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    deactivate = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    status = models.CharField(max_length=255)
    parent = models.CharField(max_length=255, null=True, blank=True)
    db_table_name = models.CharField(max_length=255, blank=True, null=True)
    origin_key = models.CharField(max_length=255, blank=True, null=True)
    bachildren = models.ForeignKey(
        TempPermissions,
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )
    is_custom_field = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    # actioned_by = models.ForeignKey(
    #     UsersModel, on_delete=models.SET_NULL, blank=True, null=True
    # )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sacco} - {self.profile} - {self.action}"


class TempFourthPermissions(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    action = models.ForeignKey(Actions, on_delete=models.SET_NULL, null=True)
    deactivate = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    status = models.CharField(max_length=255)
    parents = models.CharField(max_length=255, null=True, blank=True)
    db_table_name = models.CharField(max_length=255, blank=True, null=True)
    origin_key = models.CharField(max_length=255, blank=True, null=True)
    childrens = models.ForeignKey(
        TempSubPermissions,
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )
    is_custom_field = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    # actioned_by = models.ForeignKey(
    #     UsersModel, on_delete=models.SET_NULL, blank=True, null=True
    # )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.profile} - {self.action}"
    
    

  


