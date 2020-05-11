from rest_framework import serializers
from pwweb.resources.models import RawData

class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = '__all__'
