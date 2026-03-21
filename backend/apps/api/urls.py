from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.CurrentUserViewSet, basename="user")
router.register('posts', views.UserPostViewSet, basename="posts")
router.register('feed', views.FeedViewSet, basename='feed')


urlpatterns = [
    path("", include(router.urls)),
    path('', views.health_check, name='health-check'),
    # path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
