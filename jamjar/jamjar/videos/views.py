from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from jamjar.base.views import BaseView

from jamjar.videos.models import Video
from jamjar.videos.serializers import VideoSerializer

class VideoList(BaseView):

    serializer_class = VideoSerializer

    def get(self, request):
        videos = Video.objects.all()

        serializer = self.get_serializer(videos, many=True)
        return self.success_response(serializer.data)

    def post(self, request):
        # Initialize the serializer with our data
        self.serializer = self.get_serializer(data=request.data)

        # Validate the data
        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        # Errthang looks good.  Save it to the db
        video = self.serializer.save()

        # Return the object
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
