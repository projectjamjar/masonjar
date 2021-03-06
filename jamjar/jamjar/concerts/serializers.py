from rest_framework import serializers
from jamjar.concerts.models import Concert, SponsoredEvent
from jamjar.venues.models import Venue
from jamjar.videos.serializers import VideoSerializer
from jamjar.artists.models import Artist
from jamjar.videos.models import Video
from jamjar.artists.serializers import ArtistSerializer
from jamjar.venues.serializers import VenueSerializer
from jamjar.common.services import GMapService, ServiceError
from jamjar.videos.models import JamJarMap

import logging; logger = logging.getLogger(__name__)

class ConcertSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(required=False, read_only=True)
    venue_place_id = serializers.CharField(max_length=100,write_only=True, required=False)
    videos = serializers.SerializerMethodField()
    thumbs = serializers.SerializerMethodField()
    artists = ArtistSerializer(many=True, read_only=True)
    graph = serializers.SerializerMethodField()
    videos_count = serializers.SerializerMethodField()

    class Meta:
        model = Concert
        fields = ('id',
            'date',
            'venue_place_id',
            'venue',
            'videos',
            'artists',
            'thumbs',
            'graph',
            'videos_count',
            'jamjars_count'
        )
        read_only_fields = ('id', 'venue', 'videos')
        write_only_fields = ('venue_place_id',)

    def __init__(self, *args, **kwargs):
        # Pull out expand_videos (defaults to False)
        self.expand_videos = kwargs.pop('expand_videos', False)
        self.include_graph = kwargs.pop('include_graph', False)

        # Call super's init
        super(ConcertSerializer, self).__init__(*args, **kwargs)

        # If we don't want to expand videos, remove `videos` from the fields
        if not self.expand_videos:
            self.fields.pop('videos', None)

        if not self.include_graph:
            self.fields.pop('graph', None)

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

        (concert, created) = Concert.all_objects.get_or_create(date=date, venue=venue)

        if created:
            logger.info("New concert created {} - {}".format(venue.name, date))

        return concert

    def get_thumbs(self, obj):
        """
        Return the thumbnails from the first 3 videos in the concert (or all
        videos if there's <= 3)
        """
        first_videos = obj.videos.all()[:3]
        # import ipdb; ipdb.set_trace()
        thumbs = [video.thumb_src() for video in first_videos if video.thumb_src() is not None]
        return thumbs

    def get_graph(self, obj):
        request = self.context.get('request')
        return obj.make_graph(user=request.user)

    def get_videos_count(self, obj):
        return obj.videos.count()

    def get_videos(self, obj):
        request = self.context.get('request')
        if request.user:
            videos = obj.videos.for_user(request.user)
        else:
            videos = obj.videos.all()

        videos = videos.prefetch_related('artists',
                                         'artists__images',
                                         'artists__genres',
                                         'jamjars').select_related(
                                         'user')

        return VideoSerializer(videos, many=True, context={"request": request}).data

class SponsoredEventSerializer(serializers.ModelSerializer):
    concert = ConcertSerializer(required=True)
    artists = ArtistSerializer(required=True, many=True)

    class Meta:
        model = SponsoredEvent
        fields = ('id',
            'concert',
            'artists',
            'name'
        )
