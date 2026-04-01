import pytest
from django.urls import reverse


class TestApiCheck:
    @pytest.mark.health
    def test_api_check(self, api_client):
        URL = reverse('health-check')
        response = api_client.get(URL)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
