from rest_framework import serializers
from SessionApp.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__' #nekhdar les attribut l koul all
        