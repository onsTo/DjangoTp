from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def generate_userid():
    return "USER" + uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaines = ["esprit.tn", "sessame.com", "centarle.com", "tek.tn"]
    if email.split("@")[1] not in domaines:
        raise ValidationError("Email domain is not allowed il doit être dans les domaines suivants : esprit.tn, sessame.com, centarle.com, tek.tn")
    return email

name_validator = RegexValidator(
    regex=r'{^A-Za-z\s-}+$',  
    message="Ce champ ne peut contenir que des lettres et des espaces"
)


class User(AbstractUser):
    userid = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    firstname = models.CharField(max_length=100,validators=[name_validator])
    lastname = models.CharField(max_length=100,validators=[name_validator])
    email = models.EmailField(max_length=100, unique=True,validators=[verify_email])
    affiliation = models.CharField(max_length=225)
    nationality = models.CharField(max_length=100)
    
    Roles = [
        ('participant', 'participant'),
        ('commitee', 'Organizing commite member')
    ]
    role = models.CharField(max_length=100, choices=Roles, default="participant")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #submission = models.ManyToManyField('ConferenceApp.Conference', through="Submission")  #relation plusieurs a plusieurs avec le model submission
    #organization_commitee = models.ManyToManyField('ConferenceApp.Conference', through="Organization_commitee")  #relation plusieurs a plusieurs avec le model organization_commitee
    #ken nhb nekhdem behom na7iyou related_name

#jeya mil heritage
    def save(self, *args, **kwargs):
       
        if not self.userid:  
            new_id = generate_userid()
            while User.objects.filter(userid=new_id).exists():
                new_id = generate_userid()
            self.userid = new_id
        super().save(*args, **kwargs)


class Organization_commitee(models.Model):
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name='organization_commitee')
    conference = models.ForeignKey('ConferenceApp.Conference', on_delete=models.CASCADE, related_name='organization_commitee')
    
    Roles = [
        ('chair', 'Chair'),
        ('co-chair', 'Co-chair'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer')
    ]
    commitee_role = models.CharField(max_length=100, choices=Roles)
    date_join = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    

