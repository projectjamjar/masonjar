from rest_framework import serializers
from jamjar.videos.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'web_src', 'hls_src')
