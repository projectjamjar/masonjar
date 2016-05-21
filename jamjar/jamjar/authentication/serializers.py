from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError
from jamjar.users.models import User

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm = serializers.CharField(max_length=128)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm = attrs.get('confirm')

        if password != confirm:
            msg = 'Password does not match confirmation.'
            raise ValidationError(msg)

        return attrs

class SignupSerializer(PasswordSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    invite = serializers.CharField(max_length=50,required=False, allow_null=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        # Did we get back an active user?
        if user:
            if user.is_deleted:
                msg = ('User account has been deleted.  '
                       'Please contact support if you feel that this is incorrect.')
                raise ValidationError(msg)

            # Disable this until after spring jam
            # if not user.is_active:
            #     msg = 'User account is either not activated (check your email) or has been disabled.'
            #     raise ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            # TODO: Log invalid login here
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs

class CreateResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')

        user = get_user_model()
        exists = user.objects.filter(email=email).exists()
        attrs['exists'] = exists

        return attrs

class ResetPasswordSerializer(PasswordSerializer):
    email = serializers.EmailField(max_length=255)
    reset_key = serializers.CharField(max_length=50)

class ChangePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(max_length=128)

class ActivateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    activation_key = serializers.CharField(max_length=50)

class InviteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    message = serializers.CharField(max_length=500, required=False)

    def validate(self,data):
        # Just make sure the user doesn't already exist in the system
        user_exists = User.objects.filter(email=data.get('email'),is_active=True).exists()
        if user_exists:
            raise serializers.ValidationError('A user with this email already exists in Booksmart.')

        return data
