from jamjar.base.views import BaseView, authenticate
from jamjar.artists.models import Artist
from jamjar.artists.serializers import ArtistSerializer

class ArtistSearchView(BaseView):
    serializer_class = ArtistSerializer

    """
    Description:
        Given a search string for an artist, search spotify and return the results
        (To be used for Text Field autocompletion)

    Request:
        GET /artists/search/:search_string/

    Response:
        A list of all Artists matching that string
    """
    @authenticate
    def get(self, request, search_string):
        artists = Artist.search_artist(search_string)
        return self.success_response(artists)

class ArtistListView(BaseView):
    serializer_class = ArtistSerializer

    """
    Description:
        Given a date and a venue_place_id, get or create a concert for that combonation
        NOTE: The Date must be in ISO 8601 date format - 'YYYY-mm-dd' (2016-02-15)

    Request:
        POST /concerts/
          {
            "spotify_id": "0cmWgDlu9CwTgxPhf403hb"
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
        spotify_id = request.data.get('spotify_id')
        if spotify_id == None:
            return self.error_response("spotify_id required", 400)

        artist = Artist.get_or_create_artist(spotify_id)

        if not artist:
            return self.error_response("Unable to get or create an artist with this spotify_id", 400)

        self.serializer = self.get_serializer(artist)

        return self.success_response(self.serializer.data)