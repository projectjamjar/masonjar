from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models
from django.utils import timezone
from django.utils.http import urlquote

from jamjar.base.models import BaseModel


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, first_name, last_name):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          is_active=False,
                          first_name=first_name,
                          last_name=last_name,
                          last_login=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, first_name, last_name, password=None):
        user = self._create_user(username, email, password, first_name, last_name)
        return user


class User(AbstractUser, BaseModel):
    """
    The JamJar user model
    """
    is_deleted = models.BooleanField('deleted',
                                     default=False,
                                     help_text='Designates whether this user should be treated as '
                                               'active. Unselect this instead of deleting accounts.')
    first_login = models.BooleanField(default=True,help_text='Whether or not this is the users first login')

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def activate(self):
        """
        Set the user to active and handle any other post-activation workflow
        """
        self.is_active = True
        self.save()

        #######################################
        # Post-activation stuff
        #######################################
        # None for now
