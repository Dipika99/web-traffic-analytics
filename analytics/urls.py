from django.urls import path
from .views import TrafficLogListAPIView, home

urlpatterns = [
    path('', home, name='home'),
    path('logs/', TrafficLogListAPIView.as_view(), name='logs-list'),
]
