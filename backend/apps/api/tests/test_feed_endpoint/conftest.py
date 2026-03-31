import pytest
from backend.apps.posts.models import Post
from backend.apps.interactions.models import Comment


@pytest.fixture
def posts_created_by_followed_user(create_follow, second_user_data):
    post1 = Post.objects.create(
        title="First test post",
        body='This is first post for feed test',
        author=second_user_data
    )
    post2 = Post.objects.create(
        title="Dear Recruiters",
        body='I hope you got to this point and the second test post is visible for you',
        author=second_user_data
    )

    return post1, post2


@pytest.fixture
def third_user_post(third_user_data):
    """
    Fixture for post creation by different user
    """
    post = Post.objects.create(
        title="Post of third user",
        body='This is a post of user non-followed by current user',
        author=third_user_data
    )

    return post


@pytest.fixture
def add_comments_to_post(posts_created_by_followed_user, user_data, second_user_data):
    """
    Fixture for creating comments under a post
    """
    post1, _ = posts_created_by_followed_user
    comment1 = Comment.objects.create(
        user=user_data,
        post=post1,
        body="This post is great, I love testing it"
    )
    comment2 = Comment.objects.create(
        user=second_user_data,
        post=post1,
        body="I totally agree! Testing is amazing."
    )

    return comment1, comment2


@pytest.fixture
def post1_id(posts_created_by_followed_user):
    """
    Fixture for post1 ID
    """
    return posts_created_by_followed_user[0].id
