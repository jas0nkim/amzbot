from rest_framework import serializers
from pwweb.users.models import UserProduct

class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = '__all__'
