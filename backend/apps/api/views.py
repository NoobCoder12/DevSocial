from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.apps.posts.models import Post
from backend.apps.users.models import Profile
from django.contrib.auth.models import User
from backend.apps.interactions.models import Like, Follow, Comment
from .serializers import (
    UserSerializer,
    PostSerializer,
    LikeSerializer,
    FollowSerializer,
    CommentSerializer,
    ProfileSerializer
)
from rest_framework import viewsets
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.mixins import ListModelMixin


@extend_schema(exclude=True)    # Do not add it to Swagger
@api_view(['GET'])
@permission_classes([AllowAny])     # Overwrites permision class for this view
def health_check(request):
    return Response({'status': 'ok'})


class CurrentUserViewSet(ListModelMixin, viewsets.GenericViewSet):  # RetrieveModelMixin removed
    """
    Returns profile data of currently authenticated user.
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserPostViewSet(viewsets.ModelViewSet):
    """
    Manage posts of currently authenticated user.
    Allows creating, reading and deleting own posts.
    """
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
    Returns posts from users that current user follows.
    Use post ID to add or remove a like, or to get/add comments.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get Follow objects and follow receiver ID
        following = self.request.user.following.all().values_list("following_id", flat=True)
        # Return posts of followed users
        return Post.objects.filter(author__in=following)
    
    # Decorator for Swagger documentation, defining data type
    # 'id' is a name of variable to define
    # int is a type of defined variable
    # OpenApiParameter.PATH Where does it show up - in URL
    @extend_schema(parameters=[OpenApiParameter('id', int, OpenApiParameter.PATH)])
    # @action decorator adds action to basic URL in ViewSet
    @action(detail=True, methods=['post', 'delete', 'get'])
    # /like/ is created in URL from method name
    def like(self, request, pk=None):
        post = self.get_object()        # Gets Post object with id from URL
        if request.method == "POST":
            Like.objects.get_or_create(user=request.user, post=post)
            return Response({"message": 'Like added'}, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            Like.objects.filter(user=request.user, post=post).delete()
            return Response({"message": 'Like deleted'}, status=status.HTTP_200_OK)
        elif request.method == "GET":
            likes = Like.objects.filter(post=post)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)

    @extend_schema(parameters=[OpenApiParameter('id', int, OpenApiParameter.PATH)])
    @action(detail=True, methods=['post', 'get'])
    def comment(self, request, pk=None):
        post = self.get_object()
        if request.method == "POST":
            Comment.objects.create(user=request.user, post=post, body=request.data.get('body'))
            return Response({"message": "Comment added succesfully"}, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            comments = Comment.objects.filter(post=post)
            # Serialize objects to dictionary
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)  # Changes do JSON


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns all likes added by currently authenticated user.
    """
    serializer_class = LikeSerializer

    # Get likes of current user
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    # # Save current user as author of like while creating object
    # def perform_create(self, serializer):
    #     # Field created here should be added to read_only_fields in serializer
    #     serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns follows of current user.
    """
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns all comments added by currently authenticated user.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class SearchUsersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Search for users by username.
    Use query parameter 'q' to filter results. e.g. /search/?q=john
    Use user ID to follow or unfollow a user.
    """
    serializer_class = ProfileSerializer

    def get_queryset(self):
        # query_params is a dict with ULR parameters
        query = self.request.query_params.get("q", "")
        return Profile.objects.filter(user__username__icontains=query)

    @extend_schema(parameters=[OpenApiParameter('id', int, OpenApiParameter.PATH)])
    @action(detail=True, methods=['post', 'delete'])
    def follow(self, request, pk=None):
        followed_user = self.get_object().user  # Gets user by profile
        if request.method == "POST":
            Follow.objects.get_or_create(follower=request.user, following=followed_user)
            return Response({"message": f"User {followed_user} followed"}, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            Follow.objects.filter(follower=request.user, following=followed_user).delete()
            return Response({"message": f"User {followed_user} unfollowed"}, status=status.HTTP_204_NO_CONTENT)
