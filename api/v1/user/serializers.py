from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from user.models import BlockList, Following

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'photo'
        ]

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'photo'
        ]

        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        if password := validated_data.pop('password', None):
            instance.set_password(password)
        return super(UserDetailUpdateSerializer, self).update(instance, validated_data)


class UserBlockListSerializer(serializers.ModelSerializer):
    who_blocked = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = BlockList
        fields = [
            'who_blocked',
            'blocked_user'
        ]

    def to_internal_value(self, data):
        data = super(UserBlockListSerializer, self).to_internal_value(data)
        user = self.context.user
        data['who_blocked'] = user
        return data

    def validate(self, attrs):
        who_blocked = attrs.get('who_blocked')
        blocked_user = attrs.get('blocked_user')
        if who_blocked.id == blocked_user.id:
            raise ValidationError({"error": f"user <{who_blocked}> cannot block yourself"})
        if BlockList.objects.filter(who_blocked=who_blocked, blocked_user=blocked_user).exists():
            raise ValidationError({"unique": f"user <{who_blocked}> has already blocked user <{blocked_user}>"})
        return attrs

    def create(self, validated_data):
        who_blocked = validated_data.get('who_blocked')
        blocked_user = validated_data.get('blocked_user')
        following = Following.objects.filter(user=blocked_user, following_user=who_blocked)
        if following.exists():
            following.delete()
        return super(UserBlockListSerializer, self).create(validated_data)


class UserFollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = Following
        fields = [
            'user',
            'following_user'
        ]

    def to_internal_value(self, data):
        data = super(UserFollowSerializer, self).to_internal_value(data)
        user = self.context.user
        data['user'] = user
        return data

    def validate(self, attrs):
        user = attrs.get('user')
        following_user = attrs.get('following_user')
        if BlockList.objects.filter(who_blocked=following_user, blocked_user=user).exists():
            raise ValidationError({"error": "This user has blocked you"})
        if user.id == following_user.id:
            raise ValidationError({"error": f"user <{user}> cannot following yourself"})
        if Following.objects.filter(user=user, following_user=following_user).exists():
            raise ValidationError({"unique": f"user <{user}> has already followed user <{following_user}>"})
        return attrs


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = [
            'following_user'
        ]


class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = [
            'user'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'photo',
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'photo',
            'following',
            'followers'
        ]

    def get_following(self, obj: User):
        following = obj.following_users.all().values_list('following_user', flat=True)
        return UserDetailSerializer(User.objects.filter(id__in=following), many=True,
                                    context=self.context).data

    def get_followers(self, obj: User):
        followers = obj.followers_users.all().values_list('user', flat=True)
        return UserDetailSerializer(User.objects.filter(id__in=followers), many=True,
                                    context=self.context).data
