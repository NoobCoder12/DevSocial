from django.contrib.auth.models import User
from rest_framework import serializers
from backend.apps.posts.models import Post
from backend.apps.interactions.models import Like, Follow, Comment
from backend.apps.users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()   # DRF looks for a method named 'get_<field_name>'
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = ["id", "username", "last_login", "email", "followers_count", "following_count", "date_joined"]


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()   # DRF looks for a method named 'get_<field_name>'
    comments_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes_count()    # Model method

    def get_comments_count(self, obj):
        return obj.comments_count()

    class Meta:
        model = Post
        fields = "__all__"
        # Will not be required in POST
        read_only_fields = ['author', 'slug', 'likes_count', 'comments_count', 'date']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ["follower", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    # Show serializer where to get data from
    # Serializer doesn't accept '__'
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "username", "bio", "profile_picture"]
