from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('scrubbing.urls')),
    path('dashboard/', include('dashboard.urls')),
]
