from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIkey

class APIkeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_API_KEY")
        
        if not api_key:
            return None
        try:
            key_obj = APIkey.objects.get(key=api_key, is_active=True)
        except:
            raise AuthenticationFailed('Invalid or Non-active API-KEY')
        return(None, key_obj)
        