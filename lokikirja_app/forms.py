from django import forms
from .models import Event

class LogbookPostForm(forms.Form):
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Lisää loki'}))
    
class EventForm(forms.ModelForm):
    name = forms.CharField(label='Nimi')
    class Meta:
        model = Event
        fields = ['name']