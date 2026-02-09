import pytest
from model_bakery import baker
from datetime import datetime
from backend.apps.interactions.models import Like, Follow
from django.db import IntegrityError

# Create your tests here.


@pytest.mark.django_db(transaction=True)    # Lets Django clean up database after error to continue assertions, no TransactionManagementError
def test_like_creation_and_duplicate(user, post):
    """
    Check is like is created correctly,
    error when duplicates
    """
    like = baker.make("interactions.Like", user=user, post=post)

    assert Like.objects.count() == 1    # Manager doesn't exist for instance
    assert like.post == post
    assert like.user == user
    assert isinstance(like.created_at, datetime)

    with pytest.raises(IntegrityError):
        baker.make("interactions.Like", user=user, post=post)   # We want this error, values must be unique

    assert Like.objects.count() == 1    # To make sure there is still only one object


@pytest.mark.django_db
def test_comment_creation(user, post):
    """
    Checks if comment is created correctly
    """

    comment = baker.make("interactions.Comment", user=user, post=post)

    assert comment.user == user
    assert comment.post == post
    assert comment.body is not None
    assert isinstance(comment.created_at, datetime)


@pytest.mark.django_db(transaction=True)
def test_follow_creation(user):
    """
    Checks if follow is created correctly
    Error if follow duplicates
    Error if users tries to follow himself
    """
    user2 = baker.make("auth.User")
    follow = baker.make("interactions.Follow", follower=user, following=user2)
    assert Follow.objects.count() == 1
    assert follow.follower == user
    assert follow.following == user2
    assert isinstance(follow.created_at, datetime)

    # Calling error, duplicate
    with pytest.raises(IntegrityError):
        baker.make("interactions.Follow", follower=user, following=user2)

    # Calling error, self follow
    with pytest.raises(IntegrityError):
        baker.make("interactions.Follow", follower=user, following=user)

    assert Follow.objects.count() == 1
