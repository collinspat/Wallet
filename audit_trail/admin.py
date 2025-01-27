from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(ActivityLogs)
class ActivityLogs(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'origin', 'ip_address', 'timestamp')
    search_fields = ('user', 'action')
    list_filter = ('timestamp', 'action')   
    
    ordering = ('-id',)
