from django.contrib import admin
from .models import APIkey, SanitizationLog
# Register your models here.
class APIkeyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'key', 
        'is_active',
        'create_at'
    ]
    search_fields = [
        'name',
        'create_at'
    ]
admin.site.register(APIkey, APIkeyAdmin)

class SanitizationlogAdmin(admin.ModelAdmin):
    list_display = [
        'api_key',
        'total_detected',
        'detected_summary',
        'create_at'
    ]
    search_fields = [
        'api_key',
        'create_at'
    ]
admin.site.register(SanitizationLog, SanitizationlogAdmin)