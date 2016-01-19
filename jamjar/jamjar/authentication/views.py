from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_auth.app_settings import TokenSerializer

from jamjar.base.views import BaseView, authenticate
from jamjar.users.models import User
from jamjar.users.serializers import UserSerializer

import urllib as url
import uuid

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    CreateResetSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    ActivateSerializer,
    InviteUserSerializer
)
import emails as emails
from models import JamJarToken, UserInvite

from django.views.decorators.csrf import csrf_exempt


#############################################################################
#
# NOTE:  This is a very non-standard view.  Do not use this as an example
#  for common objects.  Authentication is handled very differently than
#  most of the other views in the application.
#
#############################################################################

class SignupView(BaseView):

    # Class vars
    serializer_class = SignupSerializer
    response_serializer = UserSerializer

    """
    Description:
        Check to see if the email is unused and return the new user object if it is not.

    Request:
        POST /api/auth/signup/
        {
            "username": "test",
            "first_name": "Test",
            "last_name": "User",
            "password": "password",
            "confirm": "password",
            "email": "test@projectjamjar.com",
            "invite": "48c-926669e40c2196dd94de"
        }

    Response:
        The new user object
    """
    def post(self, request):
        print request.data

        # Validate the request
        self.serializer = self.serializer_class(data=request.data)
        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        # Create the user
        data = request.data
        try:
            self.user = User.objects.create_user(data['username'],data['email'], data['first_name'],
                data['last_name'], data['password'])
        except IntegrityError:
            # TODO: Log signup failure here
            return self.error_response("A user with that email already exists.", 422)

        # If this user was invited by someone, handle that stuff
        if self.serializer.validated_data.get('invite'):
            token = JamJarToken.objects.get(token=self.serializer.validated_data['invite'],token_type='I')
            token.active = False
            token.save()
            invite = token.invite.get()
            invite.accepted = True
            invite.save()
            # Get all other tokens and set them to rejected
            for other_invite in UserInvite.objects.filter(email=invite.email).exclude(pk=invite.id):
                other_invite.accepted = False
                other_invite.save()
                other_token = other_invite.token
                other_token.active = False
                other_token.save()


        # This just generates us a nice token.  Not only for password resetting
        token = PasswordResetTokenGenerator().make_token(self.user)

        # Add the token to the DB
        token_object = JamJarToken(user=self.user, token=token, token_type='A', active=True)
        token_object.save()

        # The link to send the user which will prompt activation
        activate_link = "{}/auth/activate/?email={}&activation_key={}".format(settings.SITE_BASE_URL,
                                                                      url.quote(self.user.email),
                                                                      url.quote(token))

        email_info = emails.activate_account

        mail = EmailMultiAlternatives(
            subject=email_info['subject'],
            body=email_info['text'].format(activate_link=activate_link),
            from_email=email_info['from_email'],
            to=[self.user.email],
            headers=email_info['headers']
        )

        mail.attach_alternative(email_info['html'].format(activate_link=activate_link),
                                'text/html')
        if not settings.DEBUG:
            mail.send()
        else:
            self.user.activate()

        # TODO: Log signup here

        response = { 'user': self.response_serializer(self.user).data }
        return self.success_response(response)

class ActivateView(BaseView):

    serializer_class = ActivateSerializer
    """
    Description:
        Confirm that the user account for that email exists and
        is currently not active, then set them as active.

    Request:
        POST /api/auth/activate/
        {
            "email": "test@projectjamjar.com",
            "activation_key": "47o-441afc8f5d17b80ce6b7"
        }

    Response:
        The email that was activated.
    """
    def post(self, request):
        # Validate the request
        self.serializer = self.get_serializer(data=self.request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        email = self.serializer.validated_data['email']
        token = self.serializer.validated_data['activation_key']
        import ipdb; ipdb.set_trace()
        # This will fail if the user doesn't exist
        user = User.objects.get(email=email)

        # This will fail if the token is bad
        try:
            token_object = JamJarToken.objects.get(user=user, token=token, token_type='A', active=True)
        except:
            # TODO: Log error here
            return self.error_response("The supplied email did not match the activation key or there is no activation key for that account.", 403)

        # If we make it here, we gucci.  Change that password
        user.activate()

        # Deactivate the token
        token_object.active = False
        token_object.save()

        email_info = emails.activation_successful

        login_link = "{}/login?email={}".format(settings.SITE_BASE_URL,
                                                email)

        mail = EmailMultiAlternatives(
            subject=email_info['subject'],
            body=email_info['text'].format(login_link=login_link),
            from_email=email_info['from_email'],
            to=[email],
            headers=email_info['headers']
        )

        mail.attach_alternative(email_info['html'].format(login_link=login_link),
                                'text/html')
        if not settings.DEBUG:
            mail.send()

        return self.success_response('Account activation successful.')

class LoginView(BaseView):

    # Class vars
    serializer_class = LoginSerializer
    token_model = Token
    response_token_serializer = TokenSerializer
    response_user_serializer = UserSerializer

    """
    Description:
        Check the credentials and return the auth Token if the credentials are valid and authenticated.
        Calls Django Auth login method to register User ID in Django session framework

    Request:
        POST /api/auth/activate/
        {
            "username": "test",
            "password": "password"
        }

    Response:
        The user object and the REST Framework Token Object's key.
    """
    def post(self, request):
        # Validate the request
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.get_or_create(user=self.user)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

        # Build the response object
        response = {
            'token': self.response_token_serializer(self.token).data,
            'user': self.response_user_serializer(self.user).data
        }
        return self.success_response(response)


class ResetView(BaseView):

    # Class vars
    create_serializer = CreateResetSerializer
    reset_serializer = ResetPasswordSerializer

    """
    Confirm that the user account for that email exists
    and if it does then send them an email with a reset link.
    This reset link will contain a reset token which we have
    stored in the DB.

    Accept the following POST parameters:
        - email
    Return success or error
    """
    def post(self, request):
        # Validate the request
        self.serializer = self.create_serializer(data=self.request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        self.exists = self.serializer.validated_data['exists']

        if not self.exists:
            # TODO: Log error here
            return self.error_response("A user with that email was not found.", 422)

        email = self.serializer.validated_data['email']

        # A user exists with that email. Send them a reset link.

        # Get the user, then generate the reset link
        user = User.objects.get(email=email)
        token = None

        active_tokens = JamJarToken.objects.filter(user=user, active=True,token_type='R')
        if active_tokens:
            # We already have a generated token
            token = active_tokens[0].token
        else:
            token = PasswordResetTokenGenerator().make_token(user)

            # Add the token to the DB
            token_object = JamJarToken(user=user, token=token, token_type='R', active=True)
            token_object.save()

        # The link to send the user which will prompt activation
        reset_link = "{}/auth/password-reset/?email={}&reset_key={}".format(settings.SITE_BASE_URL,
                                                                      url.quote(user.email),
                                                                      url.quote(token))

        email_info = emails.password_reset

        mail = EmailMultiAlternatives(
            subject=email_info['subject'],
            body=email_info['text'].format(reset_link=reset_link),
            from_email=email_info['from_email'],
            to=[email],
            headers=email_info['headers']
        )

        mail.attach_alternative(email_info['html'].format(reset_link=reset_link),
                                'text/html')
        if not settings.DEBUG:
            mail.send()

        response = {
            'email': email
        }

        return self.success_response(response)


    """
    Confirm that the user account for that email exists
    and if it does then send them an email with a reset link.
    This reset link will contain a reset token which we have
    stored in the DB.

    Accept the following POST parameters:
        - email
    Return success or error
    """
    def put(self, request):
        # Validate the request
        self.serializer = self.reset_serializer(data=self.request.data)

        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        email = self.serializer.validated_data['email']
        token = self.serializer.validated_data['reset_key']
        new_password = self.serializer.validated_data['password']

        # This will fail if the user doesn't exist
        user = User.objects.get(email=email)

        # This will fail if the token is bad
        try:
            token_object = JamJarToken.objects.get(user=user, token=token, token_type='R', active=True)
        except:
            # TODO: Log error here
            return self.error_response("The supplied email did not match the reset token.", 403)

        # If we make it here, we gucci.  Change that password
        user.set_password(new_password)
        user.save()

        # Deactivate the token
        token_object.active = False
        token_object.save()

        email_info = emails.password_reset_success

        mail = EmailMultiAlternatives(
            subject=email_info['subject'],
            body=email_info['text'],
            from_email=email_info['from_email'],
            to=[email],
            headers=email_info['headers']
        )

        mail.attach_alternative(email_info['html'],
                                'text/html')
        if not settings.DEBUG:
            mail.send()

        response = {
            'email': email
        }

        return self.success_response(response)

class ChangePasswordView(BaseView):

    # Class vars
    serializer_class = ChangePasswordSerializer

    """
    Description:
        Check the current password and if it's correct
        then change the password to the new password.

    Request:
        POST /api/:user_id/change/
        {
            "old_password": "OldPassword",
            "passwprd": "NewStrongPassword",
            "confirm": "NewStrongPassword"
        }

    Response:
        A message saying that the password update was successful
    """
    @authenticate
    def post(self, request):
        # Validate the request
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        old_password = self.serializer.validated_data['old_password']
        new_password = self.serializer.validated_data['password']

        user = request.token.user
        correct_pw = user.check_password(old_password)

        if not correct_pw:
            return self.error_response("The provided current password does not match your password.", 403)

        # If we're here, the old password is correct.  Update the pw
        user.set_password(new_password)
        user.save()

        return self.success_response("Password successfully updated.")

class InviteUserView(BaseView):

    serializer_class = InviteUserSerializer

    """
    Description:
        Given an email and a authenticated user, send an invite to a new user

    Request:
        POST /api/:user_id/invite/
        {
            "email": "newperson@thatemail.com",
            "message": "Hey, you should join JamJar!"
        }

    Response:
        A message saying that the invite was sent successfully
    """
    @authenticate
    def post(self, request):
        # Validate the request
        self.serializer = self.serializer_class(data=self.request.data)
        if not self.serializer.is_valid():
            return self.error_response(self.serializer.errors, 400)

        # We can prep the email to send
        email = self.serializer.validated_data['email']
        message = self.serializer.validated_data.get('message')

        # A user exists with that email. Send them a reset link.

        # Get the user, then generate the reset link
        invitor = request.token.user
        invite = None

        active_invites = UserInvite.objects.filter(invitor_id=user_id, email=email)
        if active_invites:
            # We've already made a token and an invite
            invite = active_invites[0]
        else:
            invite_token = str(uuid.uuid4())

            # Add the token to the DB
            token_object = JamJarToken(user_id=user_id, token=invite_token, token_type='I', active=True)
            token_object.save()
            invite = UserInvite.objects.create(email=email,invitor_id=user_id,token=token_object,message=message)

        # The link to send the user which will prompt activation
        invite_link = "{}/auth/signup/?email={}&invite={}".format(settings.SITE_BASE_URL,
                                                                      url.quote(email),
                                                                      url.quote(invite.token.token))

        email_info = emails.invite

        email_info_text = email_info['text'].format(
            invitor_name=invitor.full_name(),
            invitor_email=invitor.email,
            message=message,
            invite_link=invite_link
        )

        email_info_html = email_info['html'].format(
            invitor_name=invitor.full_name(),
            invitor_email=invitor.email,
            message=message,
            invite_link=invite_link
        )

        mail = EmailMultiAlternatives(
            subject=email_info['subject'],
            body=email_info_text,
            from_email=email_info['from_email'],
            to=[email],
            headers=email_info['headers']
        )

        mail.attach_alternative(email_info_html,'text/html')

        if not settings.DEBUG:
            mail.send()

        response = {
            'email': email
        }

        return self.success_response("Invite sent successfully.")
