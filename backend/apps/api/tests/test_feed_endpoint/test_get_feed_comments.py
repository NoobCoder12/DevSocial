import pytest
from django.urls import reverse


class TestGetCommentsByPostId:
    @pytest.mark.feed
    def test_get_comments_by_post_id(
        self,
        add_comments_to_post,
        authorized_client,
        second_user_data,
        user_data,
        post1_id
    ):
        """
        Test for GET method for comments of chosen post
        """
        URL = reverse('feed-comment', args=[post1_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None

        assert len(data) == 2
        comment1, comment2 = data

        # Check 1st comment
        assert isinstance(comment1.get("id"), int)
        assert comment1.get("body") == 'I totally agree! Testing is amazing.'
        assert comment1.get("created_at") is not None
        assert comment1.get("user") == second_user_data.id
        assert isinstance(comment1.get("post"), int)

        # Check 2nd comment
        assert isinstance(comment2.get("id"), int)
        assert comment2.get("body") == 'This post is great, I love testing it'
        assert comment2.get("created_at") is not None
        assert comment2.get("user") == user_data.id
        assert isinstance(comment2.get("post"), int)

    @pytest.mark.feed
    def test_get_comments_by_post_id_empty(
        self,
        authorized_client,
        post1_id
    ):
        """
        Test for GET method for comments of chosen post.
        Empty list
        """
        URL = reverse('feed-comment', args=[post1_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert len(data) == 0

    @pytest.mark.feed
    def test_get_comments_by_post_id_404(
        self,
        authorized_client
    ):
        """
        Test of GET method by post ID for feed with 404 error
        """
        URL = reverse('feed-comment', args=[999])
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
        URL = reverse('feed-comment', args=[999])
        response = api_client.get(URL)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data is not None
        assert response_data.get("detail") == 'Authentication credentials were not provided.'