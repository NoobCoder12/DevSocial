import pytest
from django.urls import reverse
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class TestObtainToken:
    # Will be used in more places
    INVALID_CRED_MSG = 'No active account found with the given credentials'

    @pytest.mark.token
    def test_token(self, user_data, api_client):
        """
        Test for obtaining access and refresh token
        """
        url = reverse('token_obtain_pair')
        data = {
            "username": user_data.username,
            "password": user_data.plain_password
        }
        # DRF automatically sends data is mulipart/form-data, not JSON
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == 200
        received_data = response.json()

        # Get tokens from response
        refresh_token = received_data.get("refresh")
        access_token = received_data.get("access")

        # Check refresh token
        assert refresh_token is not None
        assert isinstance(refresh_token, str)

        # Check access token
        assert access_token is not None
        assert isinstance(access_token, str)
        print(response.headers)

    @pytest.mark.token
    def test_token_wrong_username(self, user_data, api_client):
        """
        Test for obtaining access and refresh token with wrong username
        """
        url = reverse('token_obtain_pair')
        data = {
            "username": "Wrong_username",
            "password": user_data.plain_password
        }
        # DRF automatically sends data is mulipart/form-data, not JSON
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == 401
        received_data = response.json()
        assert received_data is not None
        assert received_data.get("detail") == self.INVALID_CRED_MSG

    @pytest.mark.token
    def test_token_wrong_password(self, user_data, api_client):
        """
        Test for obtaining access and refresh token with wrong password
        """
        url = reverse('token_obtain_pair')
        data = {
            "username": user_data.username,
            "password": "TotallyRandom.123!"
        }
        # DRF automatically sends data is mulipart/form-data, not JSON
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == 401
        received_data = response.json()
        assert received_data is not None
        assert received_data.get("detail") == self.INVALID_CRED_MSG


class TestBlacklistToken:
    @pytest.mark.token
    def test_blacklist_token(self, authorized_client, logged_user_access):
        blacklisted_tokens = BlacklistedToken.objects.all()
        assert len(blacklisted_tokens) == 0

        refresh_token = logged_user_access.get("refresh")
        data = {'refresh': refresh_token}
        url = reverse("token_blacklist")
        response = authorized_client.post(url, data=data, format='json')

        assert response.status_code == 200

        blacklisted_tokens = BlacklistedToken.objects.all()
        assert len(blacklisted_tokens) == 1


class TestRefreshToken:
    @pytest.mark.token
    def test_refresh_token(
        self,
        authorized_client,
        logged_user_access
    ):
        """
        Test of generating new access token by refreshing
        """
        access_token = logged_user_access.get("access")
        refresh_token = logged_user_access.get("refresh")

        data = {'refresh': refresh_token}
        url = reverse("token_refresh")
        response = authorized_client.post(url, data=data, format='json')
        assert response.status_code == 200

        response_data = response.json()
        new_token = response_data.get("access")

        assert new_token is not None
        assert new_token != access_token

    @pytest.mark.token
    def test_refresh_with_blacklist_token(
        self,
        authorized_client,
        logged_user_access
    ):
        """
        Test of usage blacklisted token
        """

        # Blacklisting refresh token
        refresh_token = logged_user_access.get("refresh")
        data = {'refresh': refresh_token}
        url = reverse("token_blacklist")
        authorized_client.post(url, data=data, format='json')

        # Refresh blacklisted token
        refresh_url = reverse("token_refresh")
        response = authorized_client.post(refresh_url, data=data, format='json')

        # Check result
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get("detail") == 'Token is blacklisted'
        assert response_data.get("code") == 'token_not_valid'
