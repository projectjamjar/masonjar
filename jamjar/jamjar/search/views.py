from jamjar.base.views import BaseView, authenticate

from jamjar.videos.models import Video
from jamjar.users.models import User
from jamjar.venues.models import Venue
from jamjar.artists.models import Artist
from jamjar.concerts.models import Concert

from jamjar.videos.serializers import VideoSerializer
from jamjar.users.serializers import UserSerializer
from jamjar.venues.serializers import VenueSerializer
from jamjar.artists.serializers import ArtistSerializer
from jamjar.concerts.serializers import ConcertSerializer

from django.db.models import Q, query

import re, operator

MODEL_SEARCH_FIELDS = {
    Video:   ['name', 'artists__name'],
    Venue:   ['name', 'city'],
    Artist:  ['name', 'genres__name'],
    Concert: ['videos__artists__name', 'venue__name'],
    User:    ['username'],
}

MODEL_SERIALIZERS = {
    Video: VideoSerializer,
    Venue: VenueSerializer,
    Artist: ArtistSerializer,
    Concert: ConcertSerializer,
    User: UserSerializer,
}

# limit to 10 results per model
MODEL_RESULT_LIMIT = 10

class SearchResults(BaseView):

    """
    Description:
        Search videos, artists, users, concerts, and venues
        Given a query parameter, return a list of results (grouped by type)

    Request:
        GET /search/?q=World+Demo+Hip # ie. World Cafe Live, Demo Video #1, Hip-Hop artists
          The following fields are expected:
            q: The search term

    Response:
       {
          "video": [
            {
              "id": 13,
              "name": "DEMO VIDEO 1",
              "artists": [
                ...
              ],
              "thumb_src": {
                "32": "https://s3.amazonaws.com/jamjar-videos/dev/46324b43-01f3-460c-8da9-dab840b1153b/thumb-32.jpg",
                "64": "https://s3.amazonaws.com/jamjar-videos/dev/46324b43-01f3-460c-8da9-dab840b1153b/thumb-64.jpg",
                "128": "https://s3.amazonaws.com/jamjar-videos/dev/46324b43-01f3-460c-8da9-dab840b1153b/thumb-128.jpg",
                "256": "https://s3.amazonaws.com/jamjar-videos/dev/46324b43-01f3-460c-8da9-dab840b1153b/thumb-256.jpg",
                "512": "https://s3.amazonaws.com/jamjar-videos/dev/46324b43-01f3-460c-8da9-dab840b1153b/thumb-512.jpg",
                "1024": "https://s3.amazonaws.com/jamjar-videos/dev/46324b43-01f3-460c-8da9-dab840b1153b/thumb-1024.jpg"
              },
              "concert": 2,
              "user": {
                "id": 2,
                "username": "drew",
                ...
              },
            },
            ...
          ],
          "artist": [
            {
              "id": 2,
              "name": "OutKast",
              "spotify_id": "1G9G7WwrXka3Z1r7aIDjI7",
              "genres": [
                "hip hop"
              ],
              "images": [
                {
                  "url": "https://i.scdn.co/image/cf78e460a538b48dec7ef55064cdc76042511a07",
                  "height": 809,
                  "width": 1000
                },
                ...
              ],
              "unofficial": false
            }
          ],
          "venue": [
            {
              "id": 1,
              "name": "World Cafe Live",
              "place_id": "ChIJ7RhuX0_GxokRjL5qFrDINys",
              "unofficial": false,
              "formatted_address": "3025 Walnut St, Philadelphia, PA 19104, United States",
              "lat": "39.95219830",
              "lng": "-75.18517170",
              "utc_offset": -300,
              "website": "http://philly.worldcafelive.com/",
              "city": "Philadelphia",
              "state": "Pennsylvania",
              "state_short": "PA",
              "country": "United States",
              "country_short": "US"
            }
          ],
          "concert": [
            {
              "id": 1,
              "date": "2016-02-28",
              "venue": {
                "id": 1,
                "name": "World Cafe Live",
                "place_id": "ChIJ7RhuX0_GxokRjL5qFrDINys",
                "unofficial": false,
                "formatted_address": "3025 Walnut St, Philadelphia, PA 19104, United States",
                "lat": "39.95219830",
                "lng": "-75.18517170",
                "utc_offset": -300,
                "website": "http://philly.worldcafelive.com/",
                "city": "Philadelphia",
                "state": "Pennsylvania",
                "state_short": "PA",
                "country": "United States",
                "country_short": "US"
              },
              "videos": [ ... ]
              "artists": [ .. ]
            },
            ...
          ],
          "user": []
        } 
    """

    @authenticate
    def get(self, request):
        query_string = request.GET.get("q", "").strip()

        if not query_string:
            return self.error_response({"error": "Search query is empty"}, 500)

        results = self.search(query_string)
        return self.success_response(results)

    def search(self, query_string):
        data = {}

        for (model, fields) in MODEL_SEARCH_FIELDS.iteritems():
            model_name = model.__name__.lower()
            search_results = self.perform_search(query_string, model, fields)
            serializer = MODEL_SERIALIZERS[model]
            data[model_name] = serializer(search_results, many=True).data

        return data


    def normalize_query(self, query_string):
        """ match terms in quotes or non-whitespace characters
         eg: <<"hey ya" Outkast>> returns: ['hey ya', 'Outkast']
        """

        # get characters between quotes OR contiguous non-space characters
        tokens = re.findall(r'"(?:[^"]+)"|(?:\S+)', query_string)

        # remove quotes if present (they're captured above)
        return [token.replace('"', '') for token in tokens]


    def build_query(self, query_string, search_fields):
        "Builds a query from the supplied tokens"

        tokens = self.normalize_query(query_string)

        if not tokens:
            return None

        # how does this work LOL

        token_matches = []
        for token in tokens:
            token_match = (Q(**{"%s__icontains" % field_name: token}) for field_name in search_fields)
            token_matches.append(reduce(operator.__or__, token_match))

        return reduce(operator.__or__, token_matches)


    def perform_search(self, query_string, model, fields):
        """
        Perform a search in the given fields of a model or queryset
        """
        # Ensure we're dealing with a queryset
        queryset = model

        if not isinstance(queryset, query.QuerySet):
            queryset = model.objects.all()

        entry_query = self.build_query(query_string, fields)

        return queryset.filter(entry_query).distinct()[:MODEL_RESULT_LIMIT]

