from django.test import TestCase
import pytest
from model_bakery import baker
from datetime import datetime

# Create your tests here.


@pytest.mark.django_db
def test_post_creation(user, post):
    """
    Check is post is created correctly
    """

    assert post.title == "Testing"
    assert post.body is not None
    assert post.author == user
    assert isinstance(post.date, datetime)
