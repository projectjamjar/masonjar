from jamjar.base.views import BaseView, authenticate
from jamjar.users.models import User, UserBlock
from jamjar.users.serializers import UserSerializer, UserBlockSerializer
from jamjar.concerts.models import Concert
from jamjar.concerts.serializers import ConcertSerializer
from jamjar.videos.serializers import ExpandedVideoSerializer, VideoSerializer
from jamjar.videos.models import Video

class UserProfileView(BaseView):
    serializer_class = UserSerializer
    model = User

    """
    Description:
        Given a username (so that we can use the username in the client urls)
        return the user, their videos, and the concerts for those videos

    Request:
        GET /users/:username/

    Response:
        The user profile of the specified user
        {
          "user": {
            "id": 3,
            "username": "mark",
            "email": "drewbanin+mark@gmail.com",
            "first_name": "Mark",
            "last_name": "Koh",
            "full_name": "Mark Koh"
          },
          "videos": [
            {
              "id": 14,
              "name": "DEMO VIDEO 2",
              "uploaded": true,
              "uuid": "573450c4-daf7-4e08-9bed-6f9874f0d9bf",
              ....
            }
          ],
          "concerts": [
            {
              "id": 2,
              "date": "2016-02-29",
              "venue": {
                "id": 1,
                "name": "World Cafe Live",
                "place_id": "ChIJ7RhuX0_GxokRjL5qFrDINys",
                ...
              },
              "artists": [
                {
                  "id": 2,
                  "name": "OutKast",
                  "spotify_id": "1G9G7WwrXka3Z1r7aIDjI7",
                  "genres": [
                    "hip hop"
                  ],
                  "images": [
                    {
                        ...
                    }
                  ],
                  "unofficial": false
                }
              ]
            }
          ]
        }
    """

    @authenticate
    def get(self, request, username):
        logged_in_user = request.user
        user = self.get_object_or_404(self.model, username=username)

        if logged_in_user.blocks.filter(blocked_user_id=user.id).count() > 0:
            return self.error_response("User not found", 404)

        if logged_in_user.id == user.id:
            videos = Video.all_objects.filter(user_id=user.id)
        else:
            videos = user.videos.all()

        # Get a set of all concert ids which the user contributed to
        concerts = Concert.objects.filter(videos__user_id=user.id).distinct()

        user_serializer = UserSerializer(user)
        video_serializer = ExpandedVideoSerializer(videos, many=True)
        concert_serializer = ConcertSerializer(concerts, many=True, expand_videos=False)

        response = {
            'user': user_serializer.data,
            'videos': video_serializer.data,
            'concerts': concert_serializer.data
        }

        return self.success_response(response)


class UserBlockView(BaseView):
    serializer_class = UserBlockSerializer
    model = UserBlock

    @authenticate
    def get(self, request):
        self.serializer = self.get_serializer(request.user.blocks, many=True)
        return self.success_response(self.serializer.data)

    @authenticate
    def post(self, request):
        self.serializer = self.get_serializer(data=request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        data = self.serializer.validated_data

        import ipdb; ipdb.set_trace()

        return self.success_response(data)
        #VideoVote.objects.update_or_create(user_id=data['user_id'], video_id=data['video'].id, defaults={'vote': data['vote']})
        #block, created = UserBlock.objects.get_or_create(user_id=user.id, blocked_user_id=1)
