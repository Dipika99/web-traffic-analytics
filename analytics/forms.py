from django import forms
from .models import Website

class WebsiteURLForm(forms.Form):
    url = forms.URLField(label='Website URL', max_length=255)
