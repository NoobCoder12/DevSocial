import pytest
from django.urls import reverse


class TestApiCheck:
    def test_api_check(self, api_client):
        url = reverse('health-check')
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
