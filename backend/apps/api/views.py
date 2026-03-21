from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.apps.posts.models import Post
from django.contrib.auth.models import User
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
