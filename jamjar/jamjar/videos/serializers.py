from rest_framework import serializers
from jamjar.videos.models import Video, Edge
from jamjar.concerts.serializers import ConcertSerializer

import os

class VideoSerializer(serializers.ModelSerializer):
    web_src = serializers.SerializerMethodField()
    hls_src = serializers.SerializerMethodField()
    thumb_src = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id',
                  'name',
                  'uploaded',
                  'uuid',
                  'length',
                  'file_size',
                  'is_private',
                  'views',
                  'artists',
                  'tmp_src',
                  'web_src',
                  'hls_src',
                  'thumb_src',
                  'concert')

    def validate(self, data):
        data['user_id'] = self.context.get('request').token.user_id
        input_fh = self.context.get('request').FILES.get('file')

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

    def get_web_src(self, video):
        return video.web_src() if video.uploaded else None

    def get_hls_src(self, video):
        return video.hls_src() if video.uploaded else None

    def get_thumb_src(self, video):
        return video.thumb_src() if video.uploaded else None

class EdgeSerializer(serializers.ModelSerializer):
    video1 = VideoSerializer(read_only=True)
    video2 = VideoSerializer(read_only=True)

    class Meta:
        model = Edge
        fields = ('id', 'video1', 'video2', 'offset', 'confidence')
