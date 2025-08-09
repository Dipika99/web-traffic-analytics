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
            # Try to find the Website by domain
            try:
                website = Website.objects.get(domain=url)
                logs = TrafficLog.objects.filter(website=website).order_by('-timestamp')[:50]
            except Website.DoesNotExist:
                form.add_error('url', 'Website not found.')
    else:
        form = WebsiteURLForm()

    return render(request, 'analytics/home.html', {'form': form, 'logs': logs, 'website': website})
