from rest_framework import serializers

from comment.models import Comment


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

    def to_representation(self, instance: Comment):
        response = super().to_representation(instance)
        response['children'] = CommentListSerializer(instance.children.all(), many=True).data
        return response
