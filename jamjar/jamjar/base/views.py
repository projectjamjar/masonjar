from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from jamjar.base.models import *

class BaseView(GenericAPIView):

    def error_response(self, data, status):
        return ErrorResponse(data, status)

    def success_response(self, data):
        return SuccessResponse(data)

    def video_response(self, src):
        return VideoResponse(src)

    # def get(self, request, pk, format=None):
    #   return self.SuccessResponse({})
