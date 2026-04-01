import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

import django
# Initializing django before any other apps
django.setup()

import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.cache import cache
from backend.apps.interactions.models import Follow


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
def disable_debug(settings):    # Pytest-Django provides settings fixture
    settings.DEBUG = False


@pytest.fixture(autouse=True)
def disable_throttling(settings):
    """
    Disable throttling for test purpose
    """
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}

    # Reset cache counter before next test
    cache.clear()


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


@pytest.fixture
def second_authorized_client(second_user_data):
    """
    Fixture for actions for second user
    """
    client = APIClient()    # Creating second instance not to overwrite the first one
    url = reverse('token_obtain_pair')
    data = {
        "username": second_user_data.username,
        "password": second_user_data.plain_password
    }

    # DRF automatically sends data is mulipart/form-data, not JSON
    response = client.post(url, data=data, format='json')
    received_data = response.json()
    access_token = received_data.get("access")
    refresh_token = received_data.get("refresh")
    tokens = {
        "refresh": refresh_token,
        "access": access_token
    }

    # Authorize client
    access_token = tokens.get("access")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def create_post(authorized_client):
    """
    Creating single post as a fixture
    """
    post = {
        "title": "Hello recruiter",
        "body": "I hope you are satisfied with what you see"
    }

    # DRF automatically sends data is mulipart/form-data, not JSON
    response = authorized_client.post(reverse('posts-list'), data=post, format='json')

    return post, response.json()


@pytest.fixture
def create_two_posts(authorized_client):
    """
    Creating two posts as a fixture
    """
    post1 = {
        "title": "Hello recruiter",
        "body": "I hope you are satisfied with what you see"
    }

    post2 = {
        "title": "Hello recruiter",
        "body": "I hope you are satisfied with what you see"
    }

    # DRF automatically sends data is mulipart/form-data, not JSON
    response1 = authorized_client.post(reverse('posts-list'), data=post1, format='json')
    response2 = authorized_client.post(reverse('posts-list'), data=post2, format='json')

    return (post1, response1.json()), (post2, response2.json())


@pytest.fixture
def second_user_data():
    """
    Creating second user to follow
    """
    password = "Test.123!"
    user = baker.make("auth.User", username="second_user")
    user.set_password(password)
    user.save()
    user.plain_password = password  # Assigned for test purpose
    return user


@pytest.fixture
def third_user_data():
    """
    Creating third user to follow
    """
    password = "Test.123!"
    user = baker.make("auth.User", username="third_user")
    user.set_password(password)
    user.save()
    user.plain_password = password  # Assigned for test purpose
    return user


@pytest.fixture
def create_follow(user_data, second_user_data):
    """
    Creating follow
    """
    follow = Follow.objects.create(
        follower=user_data,
        following=second_user_data
    )
    return follow