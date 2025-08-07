from rest_framework import serializers
from .models import TrafficLog, Website

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'

class TrafficLogSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer(read_only=True)

    class Meta:
        model = TrafficLog
        fields = '__all__'