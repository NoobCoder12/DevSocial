import pytest
from django.urls import reverse
from backend.apps.interactions.models import Follow


@pytest.fixture
def create_second_mutual_follow(user_data, second_user_data, third_user_data):
    """
    Fixture for creating follow second user -> third user and user -> third user
    """
    follow1 = Follow.objects.create(follower=second_user_data, following=third_user_data)
    follow2 = Follow.objects.create(follower=user_data, following=third_user_data)
    return follow1, follow2


class TestAddLikesByPostId:
    @pytest.mark.feed
    def test_feed_add_like(
        self,
        authorized_client,
        user_data,
        post1_id
    ):
        """
        Test of POST method for a like with post id
        """
        # Block for checking likes
        URL = reverse('feed-like', args=[post1_id])
        response_get = authorized_client.get(URL)
        assert response_get.status_code == 200
        # Check if there is no likes before adding
        assert len(response_get.json()) == 0

        # Block for adding a like
        response_post = authorized_client.post(URL)
        assert response_post.status_code == 201
        data = response_post.json()
        assert data is not None
        assert data.get("message") == 'Like added'

        # Check likes after adding
        URL = reverse('feed-like', args=[post1_id])
        response_get_after = authorized_client.get(URL)
        assert response_get_after.status_code == 200
        data_after = response_get_after.json()
        assert len(data_after) == 1

        data_after = data_after[0]

        # Check like fields
        assert isinstance(data_after.get("id"), int)
        assert data_after.get("created_at") is not None
        assert data_after.get("user") == user_data.id
        assert data_after.get("post") == post1_id

    @pytest.mark.feed
    def test_feed_add_more_likes(
        self,
        authorized_client,
        second_authorized_client,
        create_second_mutual_follow,
        third_user_post
    ):
        """
        Test of POST method for a likes with post id
        """
        # Block for checking likes section
        post_id = third_user_post[1]    # Get id for a post of user followed by both users
        URL = reverse('feed-like', args=[post_id])
        response_get = authorized_client.get(URL)
        assert response_get.status_code == 200
        # Check if there is no likes before adding
        assert len(response_get.json()) == 0

        # Block for adding first like
        response_post = authorized_client.post(URL)
        assert response_post.status_code == 201

        # Block for adding second like
        response_post = second_authorized_client.post(URL)
        assert response_post.status_code == 201

        # Check likes after adding
        response_get = authorized_client.get(URL)
        assert response_get.status_code == 200
        assert len(response_get.json()) == 2

    @pytest.mark.feed
    def test_feed_add_likes_404(
        self,
        authorized_client
    ):
        """
        Test of POST method for a like with invalid post id
        """
        # Block for adding a like
        URL = reverse('feed-like', args=[99999])
        response_post = authorized_client.post(URL)
        assert response_post.status_code == 404
        data = response_post.json()
        assert data is not None
        assert data.get("detail") == 'No Post matches the given query.'

    @pytest.mark.feed
    def test_feed_add_like_401(
        self,
        api_client,
    ):
        """
        Test of POST method for a like with post id as unauthorized user
        """
        # Block for adding a comment
        URL = reverse('feed-like', args=[99999])
        response_post = api_client.post(URL)
        assert response_post.status_code == 401
        data = response_post.json()
        assert data is not None
        assert data.get("detail") == 'Authentication credentials were not provided.'

