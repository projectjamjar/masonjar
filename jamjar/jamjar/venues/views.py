from jamjar.base.views import BaseView, authenticate
from .models import Venue
from .serializers import VenueSerializer

class VenueSearchView(BaseView):
    serializer_class = VenueSerializer

    """
    Description:
        Given a search string for a venue, search our list of venues and return the results
        (To be used for Text Field autocompletion)

    Request:
        GET /venues/search/:search_string/

    Response:
        A list of all Venues matching that string
    """
    @authenticate
    def get(self, request, search_string):
        venues = Venue.search_venues(search_string)

        self.serializer = VenueSerializer(venues,many=True)
        return self.success_response(self.serializer.data)