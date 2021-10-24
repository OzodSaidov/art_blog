from django.db import models
from art_blog.base_model import Base
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Comment(MPTTModel):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    text = models.TextField()
