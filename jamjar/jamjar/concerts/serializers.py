from rest_framework import serializers
from jamjar.concerts.models import Concert

from jamjar.venues.serializers import VenueSerializer

class ConcertSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()

    class Meta:
        model = Concert
        fields = ('id', 'date', 'venue')

    def validate(self, data):

        return data

    # def create(self, validated_data):

    # def update(self, instance, validated_data):
