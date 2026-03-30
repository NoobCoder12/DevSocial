import pytest
from django.urls import reverse
from backend.apps.interactions.models import Follow


class TestGetSearch:
    @pytest.mark.search
    def test_get_search(self, authorized_client, second_user_data):
        """
        Test for GET method for search by query
        """
        query = second_user_data.username
        URL = reverse('search-list') + f'?q={query}'
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()[0]
        assert data is not None

        assert data.get('user') == second_user_data.id
        assert data.get("username") == query
        assert isinstance(data.get("bio"), str)
        assert data.get("profile_picture") is not None

    @pytest.mark.search
    def test_search_empty_result(self, authorized_client):
        """
        Test for GET method for missing user
        """
        URL = reverse('search-list') + f'?q=invisible-john'
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 0

    @pytest.mark.search
    def test_search_401(self, api_client):
        """
        Test for GET method as unauthorized user
        """
        URL = reverse('search-list') + f'?q=invisible-john'
        response = api_client.get(URL)
        assert response.status_code == 401
        data = response.json()
        assert data.get("detail") == 'Authentication credentials were not provided.'


class TestGetSearchById:
    @pytest.mark.search
    def test_get_by_id(self, authorized_client, second_user_data):
        """
        Test GET method by users ID
        """
        user_id = second_user_data.id
        URL = reverse("search-detail", args=[user_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None

        assert data.get("user") == user_id
        assert data.get("username") == second_user_data.username
        assert isinstance(data.get("bio"), str)
        assert data.get("profile_picture") is not None

    @pytest.mark.search
    def test_get_by_id_404(self, authorized_client):
        """
        Test GET method with wrong ID
        """
        URL = reverse("search-detail", args=[999])
        response = authorized_client.get(URL)
        assert response.status_code == 404
        data = response.json()
        assert data.get("detail") == 'No Profile matches the given query.'

    @pytest.mark.search
    def test_get_by_id_401(self, api_client):
        """
        Test for GET method as unauthorized user
        """
        URL = reverse("search-detail", args=[999])
        response = api_client.get(URL)
        assert response.status_code == 401
        data = response.json()
        assert data.get("detail") == 'Authentication credentials were not provided.'


class TestSearchFollowById:
    @pytest.mark.search
    def test_follow_by_id(self, authorized_client, user_data, second_user_data):
        """
        Test of creating follow by POST method in search endpoint
        """
        follows_before = Follow.objects.filter(follower=user_data.id, following=second_user_data.id)
        assert len(follows_before) == 0
        URL = reverse('search-follow', args=[second_user_data.id])
        response = authorized_client.post(URL)
        assert response.status_code == 201
        data = response.json()

        assert data is not None
        assert data.get("message") == f'User {second_user_data.username} followed'

        # Check db after creation
        follows_after = Follow.objects.filter(follower=user_data.id, following=second_user_data.id)
        assert len(follows_after) == 1

    @pytest.mark.search
    def test_follow_by_id_404(self, authorized_client):
        """
        Test of creating follow by POST method in search endpoint with wrong ID
        """
        URL = reverse('search-follow', args=[999])
        response = authorized_client.post(URL)
        assert response.status_code == 404
        data = response.json()
        assert data.get("detail") == 'No Profile matches the given query.'

    @pytest.mark.search
    def test_follow_by_id_401(self, api_client):
        """
        Test of creating follow by POST method in search endpoint as unauthorized user
        """
        URL = reverse('search-follow', args=[999])
        response = api_client.post(URL)
        assert response.status_code == 401
        data = response.json()
        assert data.get("detail") == 'Authentication credentials were not provided.'


class TestSearchUnfollowById:
    @pytest.fixture
    def create_follow(self, user_data, second_user_data):
        follow = Follow.objects.get_or_create(
            follower=user_data,
            following=second_user_data
        )
        return follow

    @pytest.mark.search
    def test_unfollow_by_id(
        self,
        authorized_client,
        create_follow,
        user_data,
        second_user_data
    ):
        """
        Test of DELETE method for user ID
        """
        follows_before = Follow.objects.filter(
            follower=user_data.id,
            following=second_user_data.id
        )
        assert len(follows_before) == 1
        URL = reverse('search-follow', args=[second_user_data.id])
        response = authorized_client.delete(URL)
        # Returns empty body
        assert response.status_code == 204

        # Check DB after deletion
        follows_after = Follow.objects.filter(
            follower=user_data.id,
            following=second_user_data.id
        )
        assert len(follows_after) == 0

    @pytest.mark.search
    def test_unfollow_by_id_404(self, authorized_client):
        """
        Test of deletion follow by DELETE method in search endpoint with wrong ID
        """
        URL = reverse('search-follow', args=[999])
        response = authorized_client.delete(URL)
        assert response.status_code == 404
        data = response.json()
        assert data.get("detail") == 'No Profile matches the given query.'

    @pytest.mark.search
    def test_unfollow_by_id_401(self, api_client):
        """
        Test of deletion follow by DELETE method in search endpoint as unauthorized user
        """
        URL = reverse('search-follow', args=[999])
        response = api_client.delete(URL)
        assert response.status_code == 401
        data = response.json()
        assert data.get("detail") == 'Authentication credentials were not provided.'
