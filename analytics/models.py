from django.db import models


class Website(models.Model):
    name = models.CharField(max_length=100)
    domain = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class TrafficLog(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} at {self.timestamp}"
