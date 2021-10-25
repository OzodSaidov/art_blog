from rest_framework import generics

from comment.models import Comment
from . import permissions
from api.v1.comment.serializers import CommentSerializer, CommentUpdateSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer


class CommentUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.CommentPermissions]
    serializer_class = CommentUpdateSerializer
    queryset = Comment.objects.all()
