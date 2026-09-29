from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='dashboard_index'),
    path('playground/', views.playground_view, name='dashboard_playground'),
    path('documents/', views.documents_view, name='dashboard_documents'),
    path('keys/', views.key_view, name='dashboard_keys')
]
