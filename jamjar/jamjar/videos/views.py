from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser

from jamjar.base.views import BaseView, authenticate
from jamjar.videos.models import Video, Edge
from jamjar.videos.serializers import VideoSerializer, EdgeSerializer

from django.shortcuts import redirect
from django.db.models import Q

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


        video_fh = request.FILES.get('file')

        if not video_fh:
            return self.error_response('no file given', 400)

        # This will synchronously upload the video to a temp directory then
        # queue a job to:
        # 1) transcode the video for ios and web
        # 2) upload the video to s3
        #
        # both of these things happen outside of the realm of this request!
        video_paths = Video.process_upload(video_fh)

        # tmp_src is where these are stored on disk pending transcode + s3 upload
        request.data['tmp_src'] = video_paths['tmp_src']
        request.data['hls_src'] = video_paths['hls_src']
        request.data['web_src'] = video_paths['web_src']

        # Validate the rest of the request
        self.serializer = self.get_serializer(data=request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        video = self.serializer.save()

        # do this async. TODO : change lilo to use Integers for the video_id field
        transcode_video.delay(video_paths['tmp_src'], video_paths['video_dir'], video.id)

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


class VideoGraph(BaseView):

    serializer_class = EdgeSerializer

    #@authenticate
    def get(self, request, id):
         # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
            from_video = VideoSerializer(self.video).data
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        edges = Edge.objects.filter(Q(video1_id=self.video.id) | Q(video2_id=self.video.id)).select_related('video1', 'video2')

        edges_data = []
        """
        TODO : document better....
        way to understand this:
        if offset is > 0:
            blob.video starts edge[i].offset seconds AFTER edge[i] starts
        if offset is < 0:
            blob.video starts edge[i].offset seconds BEFORE edge[i] starts
        """
        for edge in sorted(edges, key=lambda e: -e.confidence):
            data = self.get_serializer(edge).data
            if data['video1']['id'] == self.video.id:
                to_video   = data['video2']
                offset     = data['offset']
            else:
                to_video   = data['video1']
                offset     = -data['offset']

            edge_data = {
                'video'  : to_video,
                'offset' : offset,
                'confidence' : data['confidence']
            }

            edges_data.append(edge_data)

        resp = {'video' : from_video, 'edges': edges_data}
        return self.success_response(resp)

