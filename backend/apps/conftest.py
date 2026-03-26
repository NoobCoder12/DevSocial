import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

import django
# Initializing django before any other apps
django.setup()

import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from backend.config import settings
from django.urls import reverse


@pytest.fixture
def user(db):   # db needed to open connection with db
    return baker.make("auth.User", username="Test_user")


@pytest.fixture
def post(db, user):
    return baker.make("posts.Post", title="Testing", author=user)


@pytest.fixture
def api_client():
    return APIClient()  # Better compatibility with JWT tokens also with DRF


@pytest.fixture(autouse=True)
def disable_debug(settings):
    settings.DEBUG = False


@pytest.fixture
def user_data(db):
    password = "Test.123!"
    user = baker.make("auth.User", username="test_user")
    user.set_password(password)
    user.save()
    user.plain_password = password  # Assigned for test purpose
    return user


@pytest.fixture
def logged_user_access(user_data, api_client):
    url = reverse('token_obtain_pair')
    data = {
        "username": user_data.username,
        "password": user_data.plain_password
    }
    # DRF automatically sends data is mulipart/form-data, not JSON
    response = api_client.post(url, data=data, format='json')
    received_data = response.json()
    access_token = received_data.get("access")
    refresh_token = received_data.get("refresh")
    return {
        "refresh": refresh_token,
        "access": access_token
    }


@pytest.fixture
def authorized_client(logged_user_access, api_client):
    """
    Fixture for using authorized user
    """
    access_token = logged_user_access.get("access")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client

