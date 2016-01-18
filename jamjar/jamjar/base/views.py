from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from jamjar.base.models import *

from django.db.models import Q, Max
from django.shortcuts import _get_queryset
from rest_framework.exceptions import NotFound

class BaseView(GenericAPIView):

    def error_response(self, data, status):
        return ErrorResponse(data, status)

    def success_response(self, data, status=200):
        return SuccessResponse(data,status)

    def video_response(self, src):
        return VideoResponse(src)

    def get_object_or_404(self, klass, *args, **kwargs):
        """
        Uses get() to return an object, or raises a Http404 exception if the object
        does not exist.

        klass may be a Model, Manager, or QuerySet object. All other passed
        arguments and keyword arguments are used in the get() query.

        Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
        object is found.
        """
        queryset = _get_queryset(klass)
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise NotFound('A {0} with the requested ID does not exist or you do not have access to this {0}.'.format(queryset.model._meta.object_name))

def authenticate(view):
    """
    This function decorator is to be used for Class-Based view methods whcih require authentication.
    It will look for a user_id in the url parameters (denoted by `(?P<user_id>[0-9]{1,4})` in the url pattern)
    and check it against the Authorization token in the headers.  The token should take the following form:
    Key: Authorization
    Value: Token <token>
    """
    def inner(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        # user_id = kwargs.get('user_id')
        error_response = ErrorResponse('Inavlid token', 401)

        # Make sure both dependencies are set
        if not auth_header:
            return error_response

        # Make sure header follows the correct format
        tokens = auth_header.split(' ')
        if (len(tokens) != 2) or (tokens[0] != 'Token'):
            return error_response

        token = tokens[1]
        try:
            # Test the token against the userID
            request.token = Token.objects.get(key=token)
            response = view(self, request, *args, **kwargs)
            return response
        except Token.DoesNotExist:
            return error_response
    return inner