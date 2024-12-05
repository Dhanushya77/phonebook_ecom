from rest_framework import serializers
from . models import *

class Phonebook_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Phonebook
        fields = '__all__'