from django import forms
from .models import Conference

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'description', 'location', 'theme', 'start_date', 'end_date']
        labels = {
            'name': 'Nom de la conférence',
            'description': 'Description de la conférence',
            'location': 'Lieu de la conférence',
            'theme': 'Thème de la conférence',
            'start_date': 'Date de début de la conférence',
            'end_date': 'Date de fin de la conférence',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom de la conférence'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description de la conférence'}),
            'location': forms.TextInput(attrs={'placeholder': 'Lieu de la conférence'}),
            'theme': forms.Select(attrs={'placeholder': 'Thème de la conférence'}),
            'start_date': forms.DateInput(attrs={'placeholder': 'Date de début'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'Date de fin'}),
        }