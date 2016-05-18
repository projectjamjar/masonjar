from django.db import IntegrityError
from jamjar.base.views import BaseView, authenticate
from jamjar.concerts.models import Concert, SponsoredEvent
from jamjar.concerts.serializers import ConcertSerializer, SponsoredEventSerializer

import datetime

class ConcertListView(BaseView):
    serializer_class = ConcertSerializer

    """
    Description:
        Get a list of all Concerts in JamJar filtered by the following attributes:
        - venues (id)
        - dates (YYYY-MM-DD format)
        - genres (id?)
        - artists (spotify-id?)

        You may pass multiple of each filter, separated with a "+".
        These filters are accepted as query parameters in the GET URL, and are ANDed together.

    Request:
        GET /concerts/?venues=15+24+13&dates=2016-03-28&genres=1+3+6&artists=15+22

    Response:
        A list of all Concerts
    """
    @authenticate
    def get(self, request):
        # Our initial queryset is ALL concerts (this could be a lot)!
        queryset = Concert.objects.all()

        # Get all the possible filters and split them, making sure we get an
        # empty list if the parameter wasn't passed
        # (Django turns pluses into spaces)
        venue_filters = filter(None, request.GET.get('venues', '').split(' '))
        date_filters = filter(None, request.GET.get('dates', '').split(' '))
        genre_filters = filter(None, request.GET.get('genres', '').split(' '))
        artist_filters = filter(None, request.GET.get('artists', '').split(' '))

        if venue_filters:
            queryset = queryset.filter(venue_id__in=venue_filters)

        if date_filters:
            # Parse out the dates from this jawn
            parsed_dates = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in date_filters]
            queryset = queryset.filter(date__in=parsed_dates)

        if genre_filters:
            queryset = queryset.filter(videos__artists__genres__in=genre_filters)

        if artist_filters:
            queryset = queryset.filter(videos__artists__id__in=artist_filters)

        queryset = queryset.distinct().prefetch_related('artists','artists__images','artists__genres','videos','videos__jamjars').select_related('venue')

        # Serialize the requests and return them
        self.serializer = self.get_serializer(queryset, many=True)
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

class ConcertDetailView(BaseView):
    serializer_class = ConcertSerializer

    """
    Description:
        Get a Concert by id
    Request:
        GET /concerts/:id/
    Response:
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
    def get(self, request, id):
        self.concert = self.get_object_or_404(Concert, pk=id)
        self.serializer = self.get_serializer(self.concert, expand_videos=True, include_graph=True)
        return self.success_response(self.serializer.data)

class SponsoredEventView(BaseView):
    serializer_class = SponsoredEventSerializer

    """
    Description:
        Get a list of sponsored events, curated by the dopest curration team everrrr

    Request:
        GET /concerts/sponsored

    Response:
        [
            {
                "id" : 1,
                "name" : "My dope event name",
                "concert" : {...},
                "artist"  : {...}.
            },
            {
                "id" : 2,
                "name" : "My other dope event",
                "concert" : {...},
                "artist"  : {...}.
            },
            ...
        ]

    """
    @authenticate
    def get(self, request):
        queryset = SponsoredEvent.objects.all()
        self.serializer = self.get_serializer(queryset, many=True)
        return self.success_response(self.serializer.data)
