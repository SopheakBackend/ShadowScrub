from django.shortcuts import render, redirect
from django.db.models import Sum
from scrubbing.models import APIkey, SanitizationLog
from scrubbing.engine import ShadowScrubEngine

# Create your views here.
scrubber = ShadowScrubEngine()

def index_view(request):
    """
    Analytics overview page showing the amount of PII detected
    """
    total_requests = SanitizationLog.objects.count()
    total_redacted = SanitizationLog.objects.aggregate(
        Sum('total_detected')
    )['total_detected__sum'] or 0 #here we simple said total_redacted['total_detected__sum], we just write directly after the aggregate function
    #because we use Sum on total_detected field, it will return total_detected__sum with the amount of Sum value
    #so we have total_detected__sum as a key and amount of sum as a value
    
    active_key_count = APIkey.objects.filter(is_active = True).count()
    recent_logs = SanitizationLog.objects.select_related('api_key').order_by('-create_at')[:10]
    
    context = {
        'total_requests' : total_requests,
        'total_redacted' : total_redacted,
        'active_keys_count' : active_key_count,
        'recent_logs' : recent_logs
    }
    
    return render(request, 'dashboard/index.html', context)

def playground_view(request):
    """
        Playground for testing text sanitization.
    """
    
    clean_text = None
    detected_summary = None
    original_text = ""
    
    if request.method == "POST":
        original_text = request.POST.get('text', '')
        if original_text.strip():
            result = scrubber.sanitize(original_text)
            clean_text = result['clean_result']
            detected_summary = result['detected_summary']
            
            SanitizationLog.objects.create(
                total_detected = result['total_detected'],
                detected_summary = result['detected_summary']
            )
        
    return render(request, 'dashboard/playground.html', {'original_text': original_text, 'clean_text': clean_text, 'summary': detected_summary} )


def documents_view(request):
    """Page for uploading PDF/DOCX files (async scrubbing)."""
    return render(request, 'dashboard/documents.html')


def key_view(request):
    """
        Manage and generate new API keys.
    """
    if request.method == 'POST':
        key_name = request.POST.get('name', 'Default Key')
        if key_name:
            APIkey.objects.create(name=key_name)
            return redirect('dashboard_keys')
    keys = APIkey.objects.all().order_by('-create_at')
    return render(request, 'dashboard/keys.html', {'keys':keys})