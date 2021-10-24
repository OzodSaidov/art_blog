from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.v1.comment.serializers import CommentSerializer
from post.models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'image'
        ]

    def to_internal_value(self, data):
        data = super(PostSerializer, self).to_internal_value(data)
        user = self.context['request'].user
        data['author'] = user
        return data


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'image'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'image',
            'comments'
        ]

    def get_comments(self, obj: Post):
        return CommentSerializer(obj.comments.filter(parent=None), many=True).data
