from rest_framework import serializers
from jamjar.videos.models import Video, Edge
from jamjar.concerts.serializers import ConcertSerializer

import os

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'tmp_src', 'web_src', 'hls_src', 'concert')

    def validate(self, data):
        data['user_id'] = self.context.get('request').token.user_id
        input_fh = self.context.get('request').FILES.get('file')

        import ipdb; ipdb.set_trace()
        if not input_fh:
            raise serializers.ValidationError('No file given')

        if not input_fh.name:
            raise serializers.ValidationError('File unnamed?')

        extension = os.path.splitext(self.filename)[1].lower()

        if extension not in ['mp4','avi','mov']:
            raise serializers.ValidationError('Unacceptable file type: {}'.format(extension))

        # Create the filename and size with the file
        data['original_filename'] = input_fh.name
        data['file_size'] = input_fh.size
        data['file'] = input_fh
        return data

class EdgeSerializer(serializers.ModelSerializer):
    video1 = VideoSerializer(read_only=True)
    video2 = VideoSerializer(read_only=True)

    class Meta:
        model = Edge
        fields = ('id', 'video1', 'video2', 'offset', 'confidence')
