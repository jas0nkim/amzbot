from rest_framework import serializers
from pwweb.schedules.models import Job, Version

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'
