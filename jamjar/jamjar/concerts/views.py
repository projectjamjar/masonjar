from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser

from jamjar.base.views import BaseView, authenticate
from jamjar.concerts.models import Concert
from jamjar.concerts.serializers import ConcertSerializer

class ConcertGraph(BaseView):
    serializer_class = ConcertSerializer

    def get(self, request, id):
         # Attempt to get the video
        try:
            self.concert = Concert.objects.get(id=id)
        except:
            return self.error_response('Concert does not exist or you do not have access to this concert.', 404)

        concert_graph = self.concert.make_graph()
        resp = {
            "graph": concert_graph,
            "concert": ConcertSerializer(self.concert).data
        }

        return self.success_response(resp)

class ConcertListView(BaseView):
    serializer_class = ConcertSerializer

    """
    Description:
        Get a list of all Concerts in JamJar (this could be big)
    Request:
        GET /concerts/
    Response:
        A list of all Concerts
    """
    @authenticate
    def get(self, request):
        objects = Concert.objects.all()

        # Serialize the requests and return them
        self.serializer = self.get_serializer(objects, many=True)
        return self.success_response(self.serializer.data)


    """
    Description:
        Given a date and a venue_place_id, get or create a concert for that combonation
        NOTE: The Date must be in ISO 8601 date format - 'YYYY-mm-dd' (2016-02-15)

    Request:
        POST /concerts/
          {
            "venue_place_id": "ChIJPWg_kNXHxokRPXdE7nqMsI4",
            "date": "2016-02-15"
          }

    Response:
        The retrieved or created concert, with the venue serialized
        {
          "id": 1,
          "date": "2016-02-04",
          "venue": {
            "id": 1,
            "name": "Union Transfer",
            "place_id": "ChIJPWg_kNXHxokRPXdE7nqMsI4",
            "unofficial": false,
            "formatted_address": "1026 Spring Garden St, Philadelphia, PA 19123, United States",
            "lat": "39.96138760",
            "lng": "-75.15532360",
            "utc_offset": -300,
            "website": "http://www.utphilly.com/",
            "city": "Philadelphia",
            "state": "Pennsylvania",
            "state_short": "PA",
            "country": "United States",
            "country_short": "US"
          }
        }
    """
    @authenticate
    def post(self, request):
        # Validate the request
        self.serializer = self.get_serializer(data=self.request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        try:
            obj = self.serializer.save()
        except IntegrityError as e:
            return self.error_response(str(e), 400)

        return self.success_response(self.serializer.data)