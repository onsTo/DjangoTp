import string
import random
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import admin
#from .models import Submission

def validate_keywords(value):
        # Séparer les mots-clés par des virgules 
        keywords = [kw.strip() for kw in value.split(',') if kw.strip()]
        # Vérifier le nombre de mots-clés
        if len(keywords) > 10:
            raise ValidationError("Vous ne pouvez pas entrer plus de 10 mots-clés.")

def generate_submission_id():
    letters = string.ascii_uppercase
    random_str = ''.join(random.choices(letters, k=8))  # 8 lettres aléatoires
    return f"SUB-{random_str}"


class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[
        MinLengthValidator(30, message="La description doit contenir au moins 30 caractères.")
        # ou bien MinLengthValidator(limit_value=30, message="La description doit contenir au moins 30 caractères.")
    ])
    location = models.CharField(max_length=255)

    THEME = [
        ("CS&IA", "Computer science & IA"),
        ("CS", "Social science"),
        ("SE", "Science and eng")
    ]
    theme = models.CharField(max_length=255, choices=THEME)

    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #deja la fn clean() existe dans models.Model(heritage)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")
    
    #fil affichage
    def __str__(self):
        return f"{self.name} - {self.theme}"

    
class Submission(models.Model):
    submission_id = models.CharField(max_length=255, primary_key=True, unique=True, editable=False,default=generate_submission_id)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords]) 
    paper = models.FileField(upload_to='sub_paper/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    CHOICES = [
        ("Submitted", "Submitted"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Under review", "Under review"),
    ]
    status = models.CharField(max_length=255, choices=CHOICES)
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)  # corrigé
    update_at = models.DateTimeField(auto_now=True)      # corrigé
    
    userid = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='submissions')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='submissions')
    
    def clean(self):
        # 1️⃣ Vérifier que la conférence est à venir
        if self.conference.start_date < timezone.now().date():
            raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")

        # 2️⃣ Limiter le nombre de soumissions par participant par jour (ex: max 3)
        today = timezone.now().date()
        submissions_today = Submission.objects.filter(userid=self.userid, submission_date=today).exclude(pk=self.pk).count()
        if submissions_today >= 3:
            raise ValidationError("Vous avez déjà atteint le nombre maximum de 3 soumissions pour aujourd'hui.")


    
