#-------------------------------USER lqdima-------------

from django.db import models
from django.contrib.auth.models import AbstractUser #importer le modèle AbstractUser
# Create your models here.
import uuid #importer la bibliothèque uuid pour générer des identifiants uniques(chaine de car unique)

def generate_userid():
    return "USER"+uuid.uuid4().hex[:4].upper() #générer un identifiant unique de 4 caractères en majuscules



class User(AbstractUser):
    #class de type modele/ pour etre cette classe un model / le astracteUser deja hérité de ce model/(Models.Model)
    userid = models.CharField(max_length=8, primary_key=True, unique=True,editable=False) #editable=False pour que l'utilisateur ne puisse pas modifier ce champ
    firstname = models.CharField(max_length=100) #champ de type char
    lastname = models.CharField(max_length=100) #champ de type char
    email = models.EmailField(max_length=100, unique=True)  #champ de type email
    affiliation = models.CharField(max_length=225)  #champ de type char
    nationality = models.CharField(max_length=100)  #champ de type char
    Roles = [('participant', 'participant'),
    ('commitee', 'Organizing commite member')]  #liste des tuple
    
    role = models.CharField(max_length=100, choices=Roles, default="participant")  #champ de type char
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    
    #submission = models.ManyToManyField('ConferenceApp.Conference', through="Submission")  #relation plusieurs a plusieurs avec le model submission
    #organization_commitee = models.ManyToManyField('ConferenceApp.Conference', through="Organization_commitee")  #relation plusieurs a plusieurs avec le model organization_commitee
    #ken nhb nekhdem behom na7iyou related_name
    
    #methode save jeya mil heritage
    def save(self, *args, **kwargs):
    if not self.userid:  #si l'utilisateur n'a pas d'identifiant
        new_id = generate_userid()
        while User.objects.filter(userid=new_id).exists():
            new_id = generate_userid()
        self.userid = new_id
    super().save(*args, **kwargs)

class Organization_commitee(models.Model):
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name='organization_commitee')
    conference = models.ForeignKey('ConferenceApp.Conference', on_delete=models.CASCADE, related_name='organization_commitee')
    Roles = [('chair', 'Chair'),
    ('co-chair', 'Co-chair'),
    ('secretary', 'Secretary'),
    ('treasurer', 'Treasurer')]
    commitee_role = models.CharField(max_length=100, choices=Roles)  #champ de type char
    date_join = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)