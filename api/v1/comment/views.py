from rest_framework import generics

from comment.models import Comment
from . import permissions
from api.v1.comment.serializers import CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer


class CommentUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.CommentPermissions]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
