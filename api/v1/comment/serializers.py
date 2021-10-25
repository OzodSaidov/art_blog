from rest_framework import serializers
from django.contrib.auth import get_user_model
from comment.models import Comment

User = get_user_model()

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'parent',
            'text',
            'children'
        ]

        extra_kwargs = {
            'children': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'parent',
            'text',
            'children',
        ]
        extra_kwargs = {
            'children': {'read_only': True},
        }

    def to_internal_value(self, data):
        data = super(CommentSerializer, self).to_internal_value(data)
        author = self.context['request'].user
        data['author'] = author
        return data

    def to_representation(self, instance: Comment):
        response = super().to_representation(instance)
        response['children'] = CommentListSerializer(instance.children.all(), many=True).data
        return response


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text'
        ]