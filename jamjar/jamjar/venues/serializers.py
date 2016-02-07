from rest_framework import serializers
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ('id',
                  'name',
                  'place_id',
                  'unofficial',
                  'formatted_address',
                  'lat',
                  'lng',
                  'utc_offset',
                  'website',
                  'city',
                  'state',
                  'state_short',
                  'country',
                  'counry_short')
