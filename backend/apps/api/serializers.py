from django.contrib.auth.models import User
from rest_framework import serializers
from backend.apps.posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "last_login", "email", "date_joined"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        # Will not be required in POST
        read_only_fields = ['author', 'slug', 'date']
