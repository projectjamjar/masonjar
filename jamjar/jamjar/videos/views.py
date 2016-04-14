from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from django.db.models import F

from jamjar.base.views import BaseView, authenticate
from jamjar.videos.models import Video, Edge
from jamjar.videos.serializers import VideoSerializer, EdgeSerializer

from jamjar.tasks.transcode_video import transcode_video

import re, datetime

class VideoListView(BaseView):
    parser_classes = (MultiPartParser,)
    serializer_class = VideoSerializer

    """
    Description:
        Get a list of all Videos in JamJar filtered by the following attributes:
        - genres (id)
        - artists (id)
        - uploaders (id)

        A "hot" attribute can also be supplied in order to get the hot videos
        as a mix of both view count and time (and soon votes)
        (pass a 1 or 0)

        You may pass multiple of each filter, separated with a "+".
        These filters are accepted as query parameters in the GET URL, and are ANDed together.

    Request:
        GET /videos/?genres=1+3+6&artists=4+6&top=1

    Response:
        A list of all Videos meeting the criteria
    """
    @authenticate
    def get(self, request):
        # Get our inital queryset of ALL videos (this could be big!)
        queryset = Video.objects.all()

        # Get all the possible filters and split them, making sure we get an
        # empty list if the parameter wasn't passed
        # (Django turns pluses into spaces)
        genre_filters = filter(None, request.GET.get('genres', '').split(' '))
        artist_filters = filter(None, request.GET.get('artists', '').split(' '))
        uploader_filters = filter(None, request.GET.get('uploaders', '').split(' '))

        if genre_filters:
            queryset = queryset.filter(artists__genres__in=genre_filters)

        if artist_filters:
            queryset = queryset.filter(artists__in=artist_filters)

        if uploader_filters:
            queryset = queryset.filter(user__in=uploader_filters)

        hot = int(request.GET.get('hot', 0))

        if hot:
            # If "hot" is true, order by hotness
            queryset = queryset.order_by('-created_at','-views')
            now = datetime.datetime.now()
            queryset = sorted(queryset, key= lambda v: v.hot(now), reverse=True)


        serializer = self.get_serializer(queryset, many=True, include_concert=True)
        return self.success_response(serializer.data)

    """
    Description:
        Upload a video, dawg!
        Given a video, name, concert_id, and a list of artist spotify_ids, create and upload a video!

    Request:
        POST /videos/
          NOTE: This is Multipart/form data!!!!
          The following fields are expected:
            file: The file itself
            name: The name of the video (user-entered)
            concert: The ID of the concert for this video
            artists: You will have one "artists" key/value pair for every artist on this video
                yes, you may have this key MULTIPLE TIMES)
                This value will be the spotify_id of the tagged artist

    Response:
        The fresh video data for the video, including serialized artists and user!
        {
          "id": 49,
          "name": "drewww",
          "uploaded": false,
          "uuid": "dfef3693-a42f-4444-b03c-8f64e46d6b02",
          "length": null,
          "file_size": 38391947,
          "is_private": false,
          "views": 0,
          "artists": [
            {
              "id": 1,
              "name": "Bonobo",
              "spotify_id": "0cmWgDlu9CwTgxPhf403hb",
              "genres": [
                "chill-out",
                "downtempo",
                "ninja",
                "nu jazz",
                "trip hop"
              ],
              "images": [
                {
                  "url": "https://i.scdn.co/image/10e789fe4259875a0bb7f5a41f13a2c5815b4635",
                  "height": 667,
                  "width": 1000
                },
                {
                  "url": "https://i.scdn.co/image/47ca8ff0c123abac4e424fa203c9bdd14685c69e",
                  "height": 427,
                  "width": 640
                },
                {
                  "url": "https://i.scdn.co/image/1478b2e2861c22dcfa152e67581b41659ea02b47",
                  "height": 133,
                  "width": 200
                },
                {
                  "url": "https://i.scdn.co/image/165e00daafa1ae302a549c01a7a50d59e3583fb1",
                  "height": 43,
                  "width": 64
                }
              ],
              "unofficial": false
            }
          ],
          "web_src": null,
          "hls_src": null,
          "thumb_src": null,
          "concert": 1,
          "user": {
            "id": 1,
            "username": "test",
            "email": "test@user.com",
            "first_name": "Test",
            "last_name": "User",
            "full_name": "Test User"
          }
        }
    """
    @authenticate
    def post(self, request):
        # Make sure we have all of the proper attributes
        context = self.get_serializer_context()
        self.serializer = self.serializer_class(data=request.data, context=context, include_concert=True)

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
        try:
            tmp_src = video.process_upload(video_fh)
        except Exception, e:
            video.delete()
            return self.error_response(str(e), 400)

        # tmp_src is where these are stored on disk pending transcode + s3 upload
        # request.data['tmp_src'] = video_paths['tmp_src']
        # request.data['hls_src'] = video_paths['hls_src']
        # request.data['web_src'] = video_paths['web_src']
        # request.data['thumb_src'] = video_paths['thumb_src']

        # do this async. TODO : change lilo to use Integers for the video_id field
        transcode_video.delay(video.id)

        return self.success_response(self.serializer.data)


class VideoDetailsView(BaseView):

    serializer_class = VideoSerializer
    model = Video

    @authenticate
    def get(self, request, id):
        # Attempt to get the video
        self.video = self.get_object_or_404(self.model, id=id)

        # Serialize the result and return it
        self.serializer = self.get_serializer(self.video)
        return self.success_response(self.serializer.data)

    @authenticate
    def put(self, request, id):
        # Attempt to get the video
        self.video = self.get_object_or_404(self.model, id=id)

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
        self.video = self.get_object_or_404(self.model, id=id)

        # Serialize the result and return it
        self.video.delete()
        return self.success_response("Video with id {} successfully deleted.".format(id))

class VideoWatchView(BaseView):
    model = Video

    """
    Description:
        Given a video id, incremement that video count.  We want to make this
        endpoint as cheap as possible, so we do some funky stuff here.
         - We don't authenticate
         - We use an F expression to both find and update the row in the DB
           at the same time

    Request:
        POST /videos/:video_id/watching/
        {}
        (No data needed)

    Response:
        True
    """
    # Don't authenticate this
    #@authenticate
    def post(self, request, id):
        # Attempt to update the video count
        self.model.objects.filter(id=id).update(views=F('views')+1)
        return self.success_response(True)
