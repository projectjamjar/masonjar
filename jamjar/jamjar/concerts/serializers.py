from rest_framework import serializers
from jamjar.concerts.models import Concert

class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ('id', 'date', 'venue')
