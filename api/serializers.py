from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['title', ]
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ['post']
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate_following(self, following):
        if self.context.get('request').method == 'POST':
            if self.context.get('request').user == following:
                raise serializers.ValidationError(
                    'You can\'t follow to yourself.')
        return following

    class Meta:
        fields = ['user', 'following']
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following', ]
            )
        ]
        model = Follow
