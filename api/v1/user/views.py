from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.post.serializers import PostSerializer
from api.v1.user.serializers import UserCreateSerializer, UserDetailUpdateSerializer, \
    UserBlockListSerializer, UserFollowSerializer, UserInfoSerializer
from post.models import Post
from user.models import BlockList, Following

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserCreateSerializer


class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserBlockListView(APIView):

    def post(self, request, *args, **kwargs):
        status = self.request.query_params.get('status')
        if status == 'blocking':
            serializer = UserBlockListSerializer(data=self.request.data, context=self.request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"ok": "User successful added to block list"}, status=200)
        if status == 'unblocking':
            user_id = self.request.user.id
            blocked_user = self.request.data.get('blocked_user')
            block_list = BlockList.objects.filter(who_blocked=user_id, blocked_user=blocked_user)
            if block_list.exists():
                block_list.delete()
                return Response({"ok": "User successful removed from block list"}, status=200)
            else:
                return Response({"error": "This user does not exist in the block list"}, status=400)
        return Response({"status": "Status unknown"}, status=400)


class UserFollowView(APIView):

    def post(self, request, *args, **kwargs):
        status = self.request.query_params.get('status')
        if status == 'following':
            serializer = UserFollowSerializer(data=self.request.data, context=self.request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"ok": "Following successful"}, status=200)
        if status == 'unfollowing':
            user_id = self.request.user.id
            following_user_id = self.request.data.get('following_user')
            following = Following.objects.filter(user_id=user_id, following_user_id=following_user_id)
            if following.exists():
                following.delete()
                return Response({"ok": "Unfollowing successful"}, status=200)
            else:
                return Response({"error": "This user is not subscribed"}, status=400)
        return Response({"status": "Status unknown"}, status=400)


class UserInfoView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following = user.following_users.all().values_list('following_user', flat=True)
        posts = Post.objects.filter(author__in=following)
        return posts
