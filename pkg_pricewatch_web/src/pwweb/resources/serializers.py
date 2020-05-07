from rest_framework import serializers
from pwweb.resources.models import AmazonParentListing, AmazonListing, AmazonListingPrice, RawData

class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = '__all__'

class AmazonParentListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonParentListing
        fields = '__all__'

class AmazonListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonListing
        fields = '__all__'

class AmazonListingPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonListingPrice
        fields = '__all__'
