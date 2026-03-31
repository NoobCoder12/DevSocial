import pytest
from django.urls import reverse


class TestAddCommentsByPostId:
    @pytest.fixture
    def comment_body(self):
        comment = {'body': 'This is a comment added by endpoint'}
        return comment

    @pytest.mark.feed
    def test_feed_add_comment(
        self,
        authorized_client,
        user_data,
        post1_id,
        comment_body
    ):
        """
        Test of POST method for a comment with post id
        """
        # Block for checking comment section
        URL = reverse('feed-comment', args=[post1_id])
        response_get = authorized_client.get(URL)
        assert response_get.status_code == 200
        # Check if there is no comments before adding
        assert len(response_get.json()) == 0

        # Block for adding a comment
        response_post = authorized_client.post(URL, data=comment_body, format='json')
        assert response_post.status_code == 201
        data = response_post.json()
        assert data is not None
        assert data.get("message") == 'Comment added succesfully'

        # Check comments after adding
        URL = reverse('feed-comment', args=[post1_id])
        response_get_after = authorized_client.get(URL)
        assert response_get_after.status_code == 200
        data_after = response_get_after.json()
        assert len(data_after) == 1
        data_after = data_after[0]

        # Check comment fields
        assert isinstance(data_after.get("id"), int)
        assert data_after.get("body") == 'This is a comment added by endpoint'
        assert data_after.get("created_at") is not None
        assert data_after.get("user") == user_data.id
        assert isinstance(data_after.get("post"), int)

    @pytest.mark.feed
    def test_feed_add_more_comments(
        self,
        authorized_client,
        post1_id,
        comment_body
    ):
        """
        Test of POST method for a comments with post id
        """
        # Block for checking comment section
        URL = reverse('feed-comment', args=[post1_id])
        response_get = authorized_client.get(URL)
        assert response_get.status_code == 200
        # Check if there is no comments before adding
        assert len(response_get.json()) == 0

        # Block for adding first comment
        response_post = authorized_client.post(URL, data=comment_body, format='json')
        assert response_post.status_code == 201

        # Block for adding second comment
        response_post = authorized_client.post(URL, data=comment_body, format='json')
        assert response_post.status_code == 201

        # Check comments after adding
        URL = reverse('feed-comment', args=[post1_id])
        response_get = authorized_client.get(URL)
        assert response_get.status_code == 200
        assert len(response_get.json()) == 2

    @pytest.mark.feed
    def test_feed_add_comment_404(
        self,
        authorized_client,
        comment_body
    ):
        """
        Test of POST method for a comment with invalid post id
        """
        # Block for adding a comment
        URL = reverse('feed-comment', args=[99999])
        response_post = authorized_client.post(URL, data=comment_body, format='json')
        assert response_post.status_code == 404
        data = response_post.json()
        assert data is not None
        assert data.get("detail") == 'No Post matches the given query.'

    @pytest.mark.feed
    def test_feed_add_comment_401(
        self,
        api_client,
        comment_body
    ):
        """
        Test of POST method for a comment with post id as unauthorized user
        """
        # Block for adding a comment
        URL = reverse('feed-comment', args=[99999])
        response_post = api_client.post(URL, data=comment_body, format='json')
        assert response_post.status_code == 401
        data = response_post.json()
        assert data is not None
        assert data.get("detail") == 'Authentication credentials were not provided.'
