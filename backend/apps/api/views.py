from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.apps.posts.models import Post
from django.contrib.auth.models import User
from backend.apps.interactions.models import Follow
from .serializers import UserSerializer, PostSerializer
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


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get Follow objects and follow receiver ID
        following = self.request.user.following.all().values_list("following_id", flat=True)
        return Post.objects.filter(author__in=following)
