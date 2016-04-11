from jamjar.base.views import BaseView, authenticate
from jamjar.artists.models import Artist, Genre
from jamjar.artists.serializers import ArtistSerializer, GenreSerializer

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
        Get a list of all Artists in JamJar filtered by the following attributes:
        - genre

        You may pass multiple of each filter, separated with a "+".
        These filters are accepted as query parameters in the GET URL, and are ANDed together.

    Request:
        GET /artists/?genres=1+3+6

    Response:
        A list of all Artists meeting the criteria
    """
    @authenticate
    def get(self, request):
        # Our initial queryset is ALL concerts (this could be a lot)!
        queryset = Artist.objects.all()

        # Get all the possible filters and split them, making sure we get an
        # empty list if the parameter wasn't passed
        # (Django turns pluses into spaces)
        genre_filters = filter(None, request.GET.get('genres', '').split(' '))

        if genre_filters:
            queryset = queryset.filter(genres__in=genre_filters)

        queryset = queryset.distinct()

        # Serialize the requests and return them
        self.serializer = self.get_serializer(queryset, many=True)
        return self.success_response(self.serializer.data)

    """
    Description:
        Given a list of artist spotify_ids, get or create the artist in the db

    Request:
        POST /artists/
          {
            "spotify_ids": [
              "0cmWgDlu9CwTgxPhf403hb"
            ]
          }

    Response:
        The retrieved or created artist, with the genres and images serialized
        [
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
            "popularity": 70,
            "followers": 419757,
            "unofficial": false
          },

        ]
    """
    @authenticate
    def post(self, request):
        # Validate the request
        spotify_ids = request.data.get('spotify_ids')
        if spotify_ids == None:
            return self.error_response("spotify_ids required", 400)

        artists = []

        for spotify_id in spotify_ids:
          artist = Artist.get_or_create_artist(spotify_id)

          if not artist:
            return self.error_response("Unable to get or create an artist with this spotify_id: {}".format(spotify_id), 400)
          else:
            artists.append(artist)

        self.serializer = self.get_serializer(artists,many=True)

        return self.success_response(self.serializer.data)

class GenreView(BaseView):
    serializer_class = GenreSerializer

    """
    Description:
        Return a list of all genres associated with any artists in JamJar, as
        well as their respective ID's

    Request:
        GET /genres/

    Response:
        A list of all genres in jamjar
    """
    @authenticate
    def get(self, request):
        genres = Genre.objects.all()
        self.serialzier = self.get_serializer(genres, many=True)
        return self.success_response(self.serialzier.data)
