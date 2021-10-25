from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

from art_blog.base_model import Base

class User(AbstractUser):
    username = models.CharField(max_length=50,
                                unique=True,
                                error_messages={
                                    'unique': _("A user with that username already exists.")},
                                )
    email = models.EmailField(unique=True, blank=True)
    photo = models.ImageField(upload_to='user/')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        return super(User, self).get_full_name()


class BlockList(Base):
    """Блок лист"""
    who_blocked = models.ForeignKey(User, on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')

    class Meta:
        """Пользователь заблокировать другому пользователю только одинь раз"""
        constraints = [
            models.UniqueConstraint(fields=['who_blocked', 'blocked_user'], name='block_unique')
        ]


class Following(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_users')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_users')

    class Meta:
        """Пользователь подписывать другому пользователю только одинь раз"""
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name='following_unique')
        ]
