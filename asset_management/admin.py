from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Asset)
admin.site.register(Appreciation)
admin.site.register(Depreciation)
admin.site.register(Lifecycle)
admin.site.register(Maintenance)
admin.site.register(Risk)
admin.site.register(Report)

