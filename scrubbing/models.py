import secrets
from django.db import models

# Create your models here.
class APIkey(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
            super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} ({self.key})"

class SanitizationLog(models.Model):
    api_key = models.ForeignKey(APIkey,on_delete=models.SET_NULL, null=True, blank=True)
    total_detected = models.IntegerField(default=0)
    detected_summary = models.JSONField(default=dict)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Sanitization Log"
        verbose_name_plural = "Sanitization Logs"