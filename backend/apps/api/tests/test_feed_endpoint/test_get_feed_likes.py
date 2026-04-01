import pytest
from django.urls import reverse


class TestGetLikesByPostId:
    @pytest.mark.feed
    def test_get_likes_by_post_id(
        self,
        add_likes_to_post,
        authorized_client,
        second_user_data,
        user_data,
        post1_id
    ):
        """
        Test for GET method for likes of chosen post
        """
        URL = reverse('feed-like', args=[post1_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None

        assert len(data) == 2
        like1, like2 = data

        # Check 1st like
        assert isinstance(like1.get("id"), int)
        assert like1.get("created_at") is not None
        assert like1.get("user") == user_data.id
        assert like1.get("post") == post1_id

        # Check 2n like
        assert isinstance(like2.get("id"), int)
        assert like2.get("created_at") is not None
        assert like2.get("user") == second_user_data.id
        assert like2.get("post") == post1_id

    @pytest.mark.feed
    def test_get_likes_by_post_id_empty(
        self,
        authorized_client,
        post1_id
    ):
        """
        Test for GET method for likes of chosen post.
        Empty list
        """
        URL = reverse('feed-like', args=[post1_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert len(data) == 0

    @pytest.mark.feed
    def test_get_likes_by_post_id_404(
        self,
        authorized_client
    ):
        """
        Test of GET method by post ID for feed with 404 error
        """
        URL = reverse('feed-like', args=[999])
        response = authorized_client.get(URL)
        assert response.status_code == 404
        data = response.json()
        assert data is not None
        assert data.get("detail") == 'No Post matches the given query.'

    @pytest.mark.feed
    def test_get_feed_post_id_401(self, api_client):
        """
        Test of GET method by unauthorized user
        """
        URL = reverse('feed-like', args=[999])
        response = api_client.get(URL)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data is not None
        assert response_data.get("detail") == 'Authentication credentials were not provided.'
