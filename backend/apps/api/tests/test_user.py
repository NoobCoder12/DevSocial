import pytest
from django.urls import reverse


class TestCurrentUser:
    URL = reverse("user-list")

    @pytest.mark.user
    def test_get_current_user(self, authorized_client, user_data):
        """
        Test GET method on current user
        """

        response = authorized_client.get(self.URL)
        assert response.status_code == 200

        data = response.json()[0]
        assert data is not None
        assert data.get("username") == user_data.username
        assert data.get("id") == user_data.id

    @pytest.mark.user
    def test_get_current_user_401(self, api_client):
        """
        Test GET method on unauthorized user
        """
        response = api_client.get(self.URL)
        assert response.status_code == 401

        data = response.json()
        assert data is not None
        assert data.get("detail") == "Authentication credentials were not provided."
