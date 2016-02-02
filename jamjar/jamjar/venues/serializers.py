from rest_framework import serializers
from jamjar.venues.models import Venue

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('name', 'place_id', 'formatted_address', 'lat', 'lng', 'utc_offset', 'website', 'city', 'state', 'state_short', 'country', 'country_short')
