from django import forms
from .models import RTSPLink

class RTSPLinkForm(forms.ModelForm):
    class Meta:
        model = RTSPLink
        fields = ['name', 'url']
