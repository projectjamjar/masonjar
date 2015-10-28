from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from jamjar.base.views import BaseView

from rest_framework.parsers import FormParser, MultiPartParser

from jamjar.videos.models import Video
from jamjar.videos.serializers import VideoSerializer

import uuid

from django.http import HttpResponse
from wsgiref.util import FileWrapper


class VideoStream(BaseView):
    def get(self, request, id):
         # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        file = FileWrapper(open(self.video.src, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={:}'.format(self.video.src)
        return response

class VideoList(BaseView):
    parser_classes = (MultiPartParser,)
    serializer_class = VideoSerializer

    def get(self, request):
        videos = Video.objects.all()

        serializer = self.get_serializer(videos, many=True)
        return self.success_response(serializer.data)

    def post(self, request):

        if 'file' in request.FILES:
            video_fh = request.FILES['file']
        else:
            return self.error_response('no file given', 400)

        video_uid = uuid.uuid4()
        video_path = '/opt/code/masonjar/videos/{:}.mp4'.format(video_uid)

        out_fh = open(video_path, 'w')
        out_fh.write(request.FILES['file'].read())
        out_fh.close()

        # update the request src
        request.data['src'] = video_path

        self.serializer = self.get_serializer(data=request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        video = self.serializer.save()
        return self.success_response(self.serializer.data)


class VideoDetails(BaseView):

    serializer_class = VideoSerializer

    def get(self, request, id):
         # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        # Serialize the result and return it
        self.serializer = self.get_serializer(self.video)
        return self.success_response(self.serializer.data)


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


    def delete(self, request, id):
         # Attempt to get the video
        try:
            self.video = Video.objects.get(id=id)
        except:
            return self.error_response('Video does not exist or you do not have access to this video.', 404)

        # Serialize the result and return it
        self.video.delete()
        return self.success_response("Video with id {} successfully deleted.".format(id))
