from rest_framework import serializers
from jamjar.users.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'first_login')

    def __init__(self, *args, **kwargs):
        self.include_first_login = kwargs.pop('include_first_login', False)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if not self.include_first_login:
            self.fields.pop('first_login')

    def get_full_name(self, user):
        return user.get_full_name()

    def get_first_login(self, user):
        first_login = user.first_login
        # If this is the user's first time logging in, update the field
        if first_login:
            user.first_login = False
            user.save()

        return first_login
