from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import TrafficLog
from .serializers import TrafficLogSerializer
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import WebsiteURLForm
from .models import Website, TrafficLog

class TrafficLogListAPIView(generics.ListAPIView):
    queryset = TrafficLog.objects.all().order_by('-timestamp')
    serializer_class = TrafficLogSerializer


def home(request):
    logs = None
    website = None
    
    if request.method == 'POST':
        form = WebsiteURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            # Normalize the URL
            normalized_url = normalize_url(url)
            
            # Create website object (not stored in database)
            website_name = extract_website_name(normalized_url)
            website = {
                'name': website_name,
                'domain': normalized_url
            }
            
            # Generate session-based traffic logs
            logs = generate_session_traffic_logs(normalized_url)
                    
    else:
        form = WebsiteURLForm()

    return render(request, 'analytics/home.html', {
        'form': form, 
        'logs': logs, 
        'website': website
    })


def normalize_url(url):
    """Normalize URL to a standard format"""
    url = url.strip()
    
    # Add https:// if no protocol specified
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    return url


def extract_website_name(url):
    """Extract a readable name from URL"""
    import re
    
    # Remove protocol and www
    clean_url = url.replace('https://', '').replace('http://', '').replace('www.', '')
    
    # Get the domain part (before the first slash)
    domain = clean_url.split('/')[0]
    
    # Remove TLD and capitalize
    name_part = domain.split('.')[0]
    name = name_part.replace('-', ' ').replace('_', ' ').title()
    
    return name


def generate_session_traffic_logs(domain):
    """Generate session-based traffic logs (not stored in database)"""
    from django.utils import timezone
    import random
    from datetime import timedelta
    
    sample_paths = ['/', '/about', '/contact', '/products', '/services', '/blog', '/pricing', '/support']
    sample_ips = ['192.168.1.1', '10.0.0.1', '172.16.0.1', '203.0.113.1', '198.51.100.1', '185.199.108.153']
    sample_user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 11; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    ]
    sample_referrers = ['https://google.com', 'https://facebook.com', 'https://twitter.com', 'https://linkedin.com', domain, '']
    
    # Generate 5-8 sample logs with realistic timestamps
    num_logs = random.randint(5, 8)
    logs = []
    now = timezone.now()
    
    for i in range(num_logs):
        # Create logs with timestamps spread over the last few hours
        timestamp = now - timedelta(minutes=random.randint(1, 300))
        
        log = {
            'path': random.choice(sample_paths),
            'method': random.choice(['GET', 'GET', 'GET', 'GET', 'POST']),  # More GETs than POSTs
            'ip_address': random.choice(sample_ips),
            'user_agent': random.choice(sample_user_agents),
            'referrer': random.choice(sample_referrers) or '-',
            'timestamp': timestamp
        }
        logs.append(log)
    
    # Sort by timestamp (newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return logs
