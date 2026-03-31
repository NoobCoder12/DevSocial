import pytest
from django.urls import reverse


class TestGetFeedByPostId:
    @pytest.mark.feed
    def test_get_feed_post_id(
        self,
        authorized_client,
        second_user_data,
        post1_id
    ):
        """
        Test of GET method by post ID for feed
        """
        URL = reverse('feed-detail', args=[post1_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None


        # Check every field
        assert data.get("id") == post1_id
        assert isinstance(data.get("likes_count"), int)
        assert isinstance(data.get("comments_count"), int)
        assert data.get("title") == 'First test post'
        assert data.get("body") == 'This is first post for feed test'
        assert data.get("slug") is not None
        assert data.get("date") is not None
        assert data.get("author") == second_user_data.id

    @pytest.mark.feed
    def test_get_feed_post_id_404(
        self,
        authorized_client
    ):
        """
        Test of GET method by post ID for feed with 404 error
        """
        URL = reverse('feed-detail', args=[999])
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
        URL = reverse('feed-detail', args=[999])
        response = api_client.get(URL)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data is not None
        assert response_data.get("detail") == 'Authentication credentials were not provided.'