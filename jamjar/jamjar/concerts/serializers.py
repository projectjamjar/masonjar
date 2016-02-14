from rest_framework import serializers
from jamjar.concerts.models import Concert
from jamjar.venues.models import Venue
from jamjar.videos.serializers import VideoSerializer

from jamjar.venues.serializers import VenueSerializer
from jamjar.common.services import GMapService

import logging; logger = logging.getLogger(__name__)

class ConcertSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(required=False)
    venue_place_id = serializers.CharField(max_length=100,write_only=True, required=False)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Concert
        fields = ('id', 'date', 'venue_place_id', 'venue', 'videos')
        read_only_fields = ('id','venue', 'videos')
        write_only_fields = ('venue_place_id')

    def validate(self, data):

        venue_place_id = data.get('venue_place_id')

        if venue_place_id:
            venue = Venue.objects.filter(place_id=venue_place_id)

            # If the venue doesn't exist, create it
            if not venue.exists():
                try:
                    gmap = GMapService.get_place(venue_place_id)
                except ServiceError, e:
                    raise serializers.ValidationError(e.message)
                data['venue_object'] = gmap
            else:
                data['venue_object'] = venue[0]
                pass

        return data

    def create(self, validated_data):
        venue = validated_data.pop('venue_object',None)

        # Get these outta here (in case people passed them in manually)
        validated_data.pop('id',None)
        validated_data.pop('venue',None)
        validated_data.pop('venue_place_id', None)

        date = validated_data.get('date')

        if not venue:
            raise serializers.ValidationError('A venue_place_id is required for a concert')

        (concert, created) = Concert.objects.get_or_create(date=date, venue=venue)

        if created:
            logger.info("New concert created {} - {}".format(venue.name, date))

        return concert

    # def update(self, instance, validated_data):
