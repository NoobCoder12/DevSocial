import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

import django
# Initializing django before any other apps
django.setup()

import pytest
from model_bakery import baker


@pytest.fixture
def user(db):   # db needed to open connection with db
    return baker.make("auth.User", username="Test_user")


@pytest.fixture
def post(db, user):
    return baker.make("posts.Post", title="Testing", author=user)
