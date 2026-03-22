from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.apps.posts.models import Post
from django.contrib.auth.models import User
from backend.apps.interactions.models import Like, Follow, Comment
from .serializers import (
    UserSerializer,
    PostSerializer,
    LikeSerializer,
    FollowSerializer,
    CommentSerializer
)
from rest_framework import viewsets
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])     # Overwrites permision class for this view
def health_check(request):
    return Response({'status': 'ok'})


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.pk)

    # # Adds current user as author
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response({'message': 'Post created'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Here is getting the object!
        self.perform_destroy(instance)
        return Response({'message': "Post deleted"}, status=status.HTTP_200_OK)


# Only to read
class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Class allows to see posts in current user feed.
    With post ID comment and like can be created
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get Follow objects and follow receiver ID
        following = self.request.user.following.all().values_list("following_id", flat=True)
        # Return posts of followed users
        return Post.objects.filter(author__in=following)

    # @action decorator adds action to basic URL in ViewSet
    @action(detail=True, methods=['post', 'delete'])
    # /like/ is created in URL from method name
    def like(self, request, pk=None):
        post = self.get_object()        # Gets Post object with id from URL
        if request.method == "POST":
            Like.objects.get_or_create(user=request.user, post=post)
            return Response({"message": 'Like added'}, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            Like.objects.filter(user=request.user, post=post).delete()
            return Response({"message": 'Like deleted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        Comment.objects.create(user=request.user, post=post, body=request.data.get('body'))
        return Response({"message": "Comment added succesfully"}, status=status.HTTP_201_CREATED)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LikeSerializer

    # Get likes of current user
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    # # Save current user as author of like while creating object
    # def perform_create(self, serializer):
    #     # Field created here should be added to read_only_fields in serializer
    #     serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
