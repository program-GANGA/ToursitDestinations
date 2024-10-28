from rest_framework import serializers
from .models import TouristDes

class TouristDesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristDes
        fields = ['id','placename', 'weather', 'state', 'district', 'maplink', 'description', 'img']