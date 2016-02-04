from rest_framework import serializers
from jamjar.videos.models import Video, Edge
from jamjar.concerts.serializers import ConcertSerializer

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'tmp_src', 'web_src', 'hls_src', 'concert')

    def validate(self, data):
        data['user_id'] = self.context.get('request').token.user_id
        return data

class EdgeSerializer(serializers.ModelSerializer):
    video1 = VideoSerializer(read_only=True)
    video2 = VideoSerializer(read_only=True)

    class Meta:
        model = Edge
        fields = ('id', 'video1', 'video2', 'offset', 'confidence')
