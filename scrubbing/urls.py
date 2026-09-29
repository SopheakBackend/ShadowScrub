from django.urls import path
from . import views 

urlpatterns = [
    path('sanitize/text/', views.SanitizeTextView.as_view(), name='sanitize'),
    path('sanitize/file/', views.SanitizeFileView.as_view(), name='sanitize_file'),
    path('tasks/<str:task_id>/', views.TaskStatusView.as_view(), name='task_status'),
    path('export/', views.ExportScrubbedFileView.as_view(), name='export_scrubbed'),
]
