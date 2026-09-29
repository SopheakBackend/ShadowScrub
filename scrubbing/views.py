from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from celery.result import AsyncResult
from ShadowScrub.celery import app as celery_app
from rest_framework.authentication import SessionAuthentication
from django.http import HttpResponse


from .serializers import SanitizeTextSerializer
from .models import APIkey, SanitizationLog
from .authentication import APIkeyAuthentication
from .engine import ShadowScrubEngine
from .tasks import sanitize_file_async
from .exporters import export_docx_bytes, export_pdf_bytes
# Create your views here.

scrubber_engine = ShadowScrubEngine()

class SanitizeTextView(APIView):
    authentication_classes = [APIkeyAuthentication]
    
    
    def post(self, request):
        serializer = SanitizeTextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data['text']
        active_entities = serializer.validated_data['active_entities']
         
        result = scrubber_engine.sanitize(text=text, active_entities=active_entities)
        
        SanitizationLog.objects.create(
            api_key=request.auth,
            total_detected=result['total_detected'],
            detected_summary=result['detected_summary']
        )
        return Response({
            'status':"success",
            'clean_text':result['clean_result'],
            'total_detected':result['total_detected'],
            'detected_summary':result['detected_summary']
        }, status=status.HTTP_200_OK)

class SanitizeFileView(APIView):
    """Endpoint to submit .pdf or .docx files for background processing."""
    authentication_classes = [APIkeyAuthentication, SessionAuthentication]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        filename = uploaded_file.name
        if not (filename.endswith('.pdf') or filename.endswith('.docx')):
            return Response({"error": "Only .pdf and .docx files supported"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_bytes = uploaded_file.read()
        
        task = sanitize_file_async.delay(file_bytes, filename)
        
        return Response({
            "status": "processing",
            "task_id": task.id,
            "message": "File processing is being process by background worker."
        }, status=status.HTTP_202_ACCEPTED)

class TaskStatusView(APIView):
    """Endpoint used by API caller and Web JS to poll task progress."""
    authentication_classes = [APIkeyAuthentication, SessionAuthentication]
    
    def get(self, request, task_id):
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state == 'PENDING':
            return Response({'status': 'PROCESSING'}, status=status.HTTP_200_OK)
        elif task_result.state == 'SUCCESS':
            return Response({'status': 'SUCCESS', 'result': task_result.result}, status=status.HTTP_200_OK)
        elif task_result.state == 'FAILURE':
            return Response({'status': 'FAILED', 'error': str(task_result.info)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
        return Response({'status': task_result.state}, status=status.HTTP_200_OK)

class ExportScrubbedFileView(APIView):
    authentication_classes = [APIkeyAuthentication, SessionAuthentication]
    permission_classes = []

    def post(self, request):
        text = request.data.get("text", "")
        fmt = (request.data.get("format") or "").lower()  # "pdf" or "docx"

        if not text.strip():
            return Response({"error": "No text to export"}, status=status.HTTP_400_BAD_REQUEST)

        if fmt == "pdf":
            content = export_pdf_bytes(text)
            return HttpResponse(
                content,
                content_type="application/pdf",
                headers={"Content-Disposition": 'attachment; filename="scrubbed_result.pdf"'},
            )

        if fmt == "docx":
            content = export_docx_bytes(text)
            return HttpResponse(
                content,
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": 'attachment; filename="scrubbed_result.docx"'},
            )

        return Response({"error": "format must be pdf or docx"}, status=status.HTTP_400_BAD_REQUEST)