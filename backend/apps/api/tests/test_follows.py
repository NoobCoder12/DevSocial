import pytest
from django.urls import reverse
from model_bakery import baker


@pytest.fixture
def create_follow(user_data, second_user_data):
    follow = baker.make(
        'interactions.Follow',
        follower=user_data,
        following=second_user_data
    )
    return follow


@pytest.fixture
def create_two_follows(user_data, second_user_data, third_user_data):
    follow = baker.make(
        'interactions.Follow',
        follower=user_data,
        following=second_user_data
    )
    follow2 = baker.make(
        'interactions.Follow',
        follower=user_data,
        following=third_user_data
    )
    return follow, follow2


class TestGetFollows:
    URL = reverse("follows-list")

    @pytest.mark.follow
    def test_get_follows(self, authorized_client, create_follow, user_data, second_user_data):
        """
        Test of GET method for current user follows
        """
        response = authorized_client.get(self.URL)
        assert response.status_code == 200

        data = response.json()
        assert data is not None
        assert len(data) == 1
        data = data[0]

        assert data.get("id") is not None
        assert data.get("created_at") is not None
        assert data.get("follower") == user_data.id
        assert data.get("following") == second_user_data.id

    @pytest.mark.follow
    def test_get_2_follows(self, authorized_client, create_two_follows):
        """
        Test of GET method for current user follows.
        Returns len == 2
        """
        response = authorized_client.get(self.URL)
        assert response.status_code == 200

        data = response.json()
        assert data is not None
        assert len(data) == 2

    @pytest.mark.follow
    def test_get_follows_401(self, api_client):
        """
        Test of GET method as unauthorized user
        """
        response = api_client.get(self.URL)
        assert response.status_code == 401
        data = response.json()

        assert data is not None
        assert data.get("detail") == "Authentication credentials were not provided."


class TestGetFollowById:
    @pytest.mark.follow
    def test_get_follow_by_id(self, authorized_client, create_follow, user_data, second_user_data):
        """
        Test of GET method on a follow by its ID
        """
        # Get id for URL
        follow_id = create_follow.id
        URL = reverse("follows-detail", args=[follow_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200

        data = response.json()
        assert data is not None

        # Check every field
        assert data.get("id") == follow_id
        assert data.get("created_at") is not None
        assert data.get("follower") == user_data.id
        assert data.get("following") == second_user_data.id

    @pytest.mark.follow
    def test_get_follow_404(self, authorized_client):
        """
        Test of GET method on a follow by non-existent ID
        """
        URL = reverse("follows-detail", args=[999])
        response = authorized_client.get(URL)
        assert response.status_code == 404

        data = response.json()
        assert data is not None
        assert data.get("detail") == 'No Follow matches the given query.'

    @pytest.mark.follow
    def test_get_follow_401(self, api_client):
        """
        Test of GET method by unauthorized user
        """
        URL = reverse("follows-detail", args=[999])
        response = api_client.get(URL)
        assert response.status_code == 401

        data = response.json()
        assert data is not None
        assert data.get("detail") == "Authentication credentials were not provided."
