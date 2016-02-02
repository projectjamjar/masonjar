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
