from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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


class User(AbstractBaseUser, BaseModel):
    """
    The JamJar user model
    """
    username = models.CharField('username', max_length=25, unique=True)
    email = models.EmailField('email address', max_length=100, unique=True)
    first_name = models.CharField('first name', max_length=50, blank=True)
    last_name = models.CharField('last name', max_length=50, blank=True)
    is_active = models.BooleanField('active',
                                    default=False,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Will be true once user has activated their account.')
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

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

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

    def full_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name