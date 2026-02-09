import pytest
from model_bakery import baker

# Create your tests here.


@pytest.mark.django_db
def test_user_profile_creation():
    """
    Check is user is created correctly
    """
    user = baker.make('auth.User', username="Test")

    assert user.username == "Test"
    assert user.is_active is True
    assert user.id is not None
