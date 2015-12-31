from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_login = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'first_login')

    def get_full_name(self, user):
        return user.full_name()

    def get_first_login(self, user):
        first_login = user.first_login
        # If this is the user's first time logging in, update the field
        if first_login:
            user.first_login = False
            user.save()

        return first_login
