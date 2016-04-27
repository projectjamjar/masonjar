from rest_framework import serializers
from jamjar.videos.models import Video, Edge
from jamjar.artists.serializers import ArtistSerializer
from jamjar.users.serializers import UserSerializer
from jamjar.artists.models import Artist

import os

class VideoSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True, include_first_login=True)

    class Meta:
        model = Video
        fields = ('id',
                  'name',
                  'uploaded',
                  'created_at',
                  'uuid',
                  'length',
                  'file_size',
                  'is_private',
                  'views',
                  'artists',
                  'web_src',
                  'hls_src',
                  'thumb_src',
                  'concert',
                  'user',
                  'width',
                  'height')

    def __init__(self, *args, **kwargs):
        super(VideoSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        request = self.context.get('request')
        data['user_id'] = request.token.user_id
        input_fh = self.context.get('request').FILES.get('file')

        # Get the artists from the request!
        if request.data.get('artists'):
            artists = request.data.getlist('artists')
            # Get the artist objects and filter out the Nones if there are any
            data['artist_objects'] = [artist for artist in [Artist.get_or_create_artist(artist) for artist in artists] if artist]

        if not input_fh:
            raise serializers.ValidationError('No file given')

        if not input_fh.name:
            raise serializers.ValidationError('File unnamed?')

        extension = os.path.splitext(input_fh.name)[1].lower()

        if extension not in ['.mp4','.avi','.mov']:
            raise serializers.ValidationError('Unacceptable file type: {}'.format(extension))

        # Create the filename and size with the file
        data['original_filename'] = input_fh.name
        data['file_size'] = input_fh.size
        data['file'] = input_fh

        return data

    def create(self,validated_data):
        # Get the artists out of here beforehand
        artists = validated_data.pop('artist_objects',[])

        # Call the super's 'create'

        video = super(VideoSerializer,self).create(validated_data)

        # Assign the artists to the video
        video.artists = artists

        return video


class ExpandedVideoSerializer(VideoSerializer):
    class Meta:
        model = Video
        fields = ('id',
                  'name',
                  'uploaded',
                  'created_at',
                  'uuid',
                  'length',
                  'file_size',
                  'is_private',
                  'views',
                  'artists',
                  'web_src',
                  'hls_src',
                  'thumb_src',
                  'concert',
                  'user',
                  'width',
                  'height')

    def __init__(self, *args, **kwargs):
        super(ExpandedVideoSerializer, self).__init__(*args, **kwargs)

        from jamjar.concerts.serializers import ConcertSerializer
        self.fields['concert'] = ConcertSerializer(read_only=True)

class EdgeSerializer(serializers.ModelSerializer):
    video1 = VideoSerializer(read_only=True)
    video2 = VideoSerializer(read_only=True)

    class Meta:
        model = Edge
        fields = ('id', 'video1', 'video2', 'offset', 'confidence')
