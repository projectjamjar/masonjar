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
        POST /artists/
          {
            "spotify_id": "0cmWgDlu9CwTgxPhf403hb"
          }

    Response:
        The retrieved or created artist, with the genres and images serialized
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
