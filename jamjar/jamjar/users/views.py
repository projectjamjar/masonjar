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
        Given a date and a venue_place_id, get or create a concert for that combonation
        NOTE: The Date must be in ISO 8601 date format - 'YYYY-mm-dd' (2016-02-15)

    Request:
        GET /users/:username/

    Response:
        The user profile of the specified user
    """

    @authenticate
    def get(self, request, username):
        user = self.get_object_or_404(self.model, username=username)

        videos = user.videos.all()

        # Get a set of all concert ids which the user contributed to
        concert_ids = set(videos.values_list('concert_id',flat=True))
        concerts = Concert.objects.filter(id__in=concert_ids)

        user_serializer = UserSerializer(user)
        video_serializer = VideoSerializer(videos, many=True)
        concert_serializer = ConcertSerializer(concerts, many=True, expand_videos=False)

        response = {
            'user': user_serializer.data,
            'videos': video_serializer.data,
            'concerts': concert_serializer.data
        }

        return self.success_response(response)