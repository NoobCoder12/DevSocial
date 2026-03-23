from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from rest_framework.routers import DefaultRouter
from debug_toolbar.toolbar import debug_toolbar_urls

router = DefaultRouter()
router.register('user', views.CurrentUserViewSet, basename="user")
router.register('posts', views.UserPostViewSet, basename="posts")
router.register('feed', views.FeedViewSet, basename='feed')
router.register('likes', views.LikeViewSet, basename='likes')
router.register('follows', views.FollowViewSet, basename="follows")
router.register('comments', views.CommentViewSet, basename="comments")
router.register('search', views.SearchUsersViewSet, basename='search')

urlpatterns = [
    path("", include(router.urls)),
    path('', views.health_check, name='health-check'),
    # Generates raw OpenAPI schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Gets the schema and renders as UI
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),   # url_name is a schema hint
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Refresh token is sent to a black list, new table with blacklisted tokens is created
    # Access token (15min) remains valid until expiry.
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] + debug_toolbar_urls()
