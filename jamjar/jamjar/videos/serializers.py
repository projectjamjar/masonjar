from rest_framework import serializers
from jamjar.videos.models import Video, Edge

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'tmp_src', 'web_src', 'hls_src', 'concert')

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ('id', 'video1', 'video2', 'offset', 'confidence')
