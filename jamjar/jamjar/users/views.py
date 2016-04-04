from jamjar.base.views import BaseView, authenticate
from jamjar.users.models import User
from jamjar.users.serializers import UserSerializer
from jamjar.concerts.models import Concert
from jamjar.concerts.serializers import ConcertSerializer
from jamjar.videos.serializers import VideoSerializer

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
        user = self.get_object_or_404(self.model, username=username)

        videos = user.videos.all()

        # Get a set of all concert ids which the user contributed to
        concerts = Concert.objects.filter(videos__user_id=user.id)

        user_serializer = UserSerializer(user)
        video_serializer = VideoSerializer(videos, many=True)
        concert_serializer = ConcertSerializer(concerts, many=True, expand_videos=False)

        response = {
            'user': user_serializer.data,
            'videos': video_serializer.data,
            'concerts': concert_serializer.data
        }

        return self.success_response(response)