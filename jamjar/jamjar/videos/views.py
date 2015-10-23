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