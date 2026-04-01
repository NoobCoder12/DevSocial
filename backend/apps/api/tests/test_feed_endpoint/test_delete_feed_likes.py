import pytest
from django.urls import reverse
from backend.apps.interactions.models import Like
from backend.apps.posts.models import Post


@pytest.fixture
def create_like(user_data, post1_id):
    """
    Fixture for creating like under one post
    """
    post = Post.objects.get(id=post1_id)
    like = Like.objects.create(user=user_data, post=post)
    return like


class TestDeleteLikesByPostId:
    @pytest.mark.feed
    def test_delete_feed_likes(self, create_like, authorized_client, post1_id):
        """
        Test for DELETE method for like in feed
        """
        # Check data first
        URL_POST = reverse('feed-detail', args=[post1_id])
        response_before = authorized_client.get(URL_POST)
        assert response_before.status_code == 200
        assert response_before.json().get('likes_count') == 1

        # Delete like
        URL_DELETE = reverse('feed-like', args=[post1_id])
        response_delete = authorized_client.delete(URL_DELETE)
        assert response_delete.status_code == 200
        data = response_delete.json()
        assert data is not None
        assert data.get("message") == "Like deleted"

        # Check after
        response_before = authorized_client.get(URL_POST)
        assert response_before.status_code == 200
        assert response_before.json().get('likes_count') == 0

    @pytest.mark.feed
    def test_feed_delete_likes_404(
        self,
        authorized_client
    ):
        """
        Test of DELETE method for a like with invalid post id
        """
        URL = reverse('feed-like', args=[99999])
        response_post = authorized_client.delete(URL)
        assert response_post.status_code == 404
        data = response_post.json()
        assert data is not None
        assert data.get("detail") == 'No Post matches the given query.'

    @pytest.mark.feed
    def test_feed_delete_like_401(
        self,
        api_client,
    ):
        """
        Test of DELETE method for a like with post id as unauthorized user
        """
        URL = reverse('feed-like', args=[99999])
        response_post = api_client.delete(URL)
        assert response_post.status_code == 401
        data = response_post.json()
        assert data is not None
        assert data.get("detail") == 'Authentication credentials were not provided.'
