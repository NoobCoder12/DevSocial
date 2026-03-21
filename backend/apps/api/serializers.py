from django.contrib.auth.models import User
from rest_framework import serializers
from backend.apps.posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()   # DRF ignores "get_" and sends the value to proper variable
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = ["id", "username", "last_login", "email", "followers_count", "following_count", "date_joined"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        # Will not be required in POST
        read_only_fields = ['author', 'slug', 'date']
