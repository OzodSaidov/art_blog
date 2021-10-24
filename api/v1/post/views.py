from rest_framework import generics
from . import permissions
from api.v1.post.serializers import PostSerializer, PostListSerializer, PostDetailSerializer
from post.models import Post


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDetailUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.PostPermission]
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
