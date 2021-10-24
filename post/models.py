from django.db import models

from art_blog.base_model import Base


class Post(Base):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post/')
