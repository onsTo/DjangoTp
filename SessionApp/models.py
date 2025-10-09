from django.db import models
from ConferenceApp.models import Conference
from django.core.validators import RegexValidator

room_validator = RegexValidator(r'^[A-Za-z0-9\s]+$', 'Room may contain only letters, numbers and spaces')


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room=models.CharField(max_length=100,validators=[room_validator])
    
    created_at = models.DateTimeField(auto_now_add=True)  # corrigé
    update_at = models.DateTimeField(auto_now=True)      # corrigé
    
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='sessions')
