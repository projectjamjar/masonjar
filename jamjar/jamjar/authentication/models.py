from django.db import models

from jamjar.users.models import User
from jamjar.base.models import BaseModel

TOKEN_TYPES = (
    ('R','password reset'),
    ('A','activation'),
    ('I','invite')
)

class JmaJarToken(BaseModel):
    # The user that this token corresponds to
    user = models.ForeignKey(User)

    # The actual token value
    token = models.CharField(max_length=50)

    # This value is used if a explicit permission does not exist for a role
    # (e.g: if a new entity was added after the role was created)
    token_type = models.CharField('Type of token',
                                          max_length=1,
                                          choices=TOKEN_TYPES)

    active = models.BooleanField(default=False)

    # test = models.BooleanField(default=True)

    class Meta:
        unique_together = (('token','token_type',),)

class UserInvite(BaseModel):
    email = models.EmailField(max_length=255)
    invitor = models.ForeignKey(User,related_name='sent_invites')
    token = models.ForeignKey(BooksmartToken,related_name='invite')
    message = models.CharField(max_length=500)
    accepted = models.NullBooleanField(null=True)
