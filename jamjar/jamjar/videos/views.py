from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser

from jamjar.base.views import BaseView, authenticate
from jamjar.videos.models import Video, Edge
from jamjar.videos.serializers import VideoSerializer, EdgeSerializer

from django.shortcuts import redirect

from jamjar.tasks.transcode_video import transcode_video

import re

class VideoList(BaseView):
    parser_classes = (MultiPartParser,)
    serializer_class = VideoSerializer

    @authenticate
    def get(self, request):
        videos = Video.objects.all()

        serializer = self.get_serializer(videos, many=True)
        return self.success_response(serializer.data)

    @authenticate
    def post(self, request):

        # Make sure we have all of the proper attributes
        self.serializer = self.get_serializer(data=request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        video_fh = self.serializer.validated_data.pop('file')

        # Create the video object so we can get the UUID and paths
        video = self.serializer.save()


        # This will synchronously upload the video to a temp directory then
        # queue a job to:
        # 1) transcode the video for ios and web
        # 2) upload the video to s3
        #
        # both of these things happen outside of the realm of this request!
        tmp_src = video.process_upload(video_fh)

        # tmp_src is where these are stored on disk pending transcode + s3 upload
        # request.data['tmp_src'] = video_paths['tmp_src']
        # request.data['hls_src'] = video_paths['hls_src']
        # request.data['web_src'] = video_paths['web_src']
        # request.data['thumb_src'] = video_paths['thumb_src']

        # do this async. TODO : change lilo to use Integers for the video_id field
        transcode_video.delay(video.id)

        return self.success_response(self.serializer.data)


class VideoDetails(BaseView):

    serializer_class = VideoSerializer

    @authenticate
    def get(self, request, id):
         # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        # Serialize the result and return it
        self.serializer = self.get_serializer(self.video)
        return self.success_response(self.serializer.data)

    @authenticate
    def put(self, request, id):
        # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        # Initialize the serializer with our data
        self.serializer = self.get_serializer(self.video, data=request.data)

        # Validate the data
        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        # Errthang looks good.  Save it to the db
        video = self.serializer.save()
        return self.success_response(self.serializer.data)

    @authenticate
    def delete(self, request, id):
         # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        # Serialize the result and return it
        self.video.delete()
        return self.success_response("Video with id {} successfully deleted.".format(id))

