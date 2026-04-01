import pytest
from django.urls import reverse
from model_bakery import baker
from backend.apps.posts.models import Post


@pytest.fixture
def create_like(create_post, user_data):
    """
    Fixture for like creation
    """
    post_id = create_post[1].get("id")
    post = Post.objects.get(id=post_id)
    like = baker.make(
        'interactions.Like',
        user=user_data,
        post=post
    )
    return like


@pytest.fixture
def create_two_likes(create_two_posts, user_data):
    """
    Fixture for 2 likes creation
    """
    post1, post2 = create_two_posts
    post1_id = post1[1].get("id")
    post2_id = post2[1].get("id")
    post1_obj = Post.objects.get(id=post1_id)
    post2_obj = Post.objects.get(id=post2_id)
    like1 = baker.make(
        'interactions.Like',
        user=user_data,
        post=post1_obj
    )
    like2 = baker.make(
        'interactions.Like',
        user=user_data,
        post=post2_obj
    )
    return like1, like2


class TestGetLikes:
    URL = reverse("likes-list")

    @pytest.mark.like
    def test_get_user_likes(self, authorized_client, create_like, user_data):
        """
        Test of GET method for current user likes
        """
        response = authorized_client.get(self.URL)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        data = data[0]
        assert data is not None
        assert data.get("id") is not None
        assert data.get("created_at") is not None
        assert data.get("user") == user_data.id
        assert data.get("post") == create_like.post.id

    @pytest.mark.like
    def test_get_user_two_likes(self, authorized_client, create_two_likes):
        """
        Test of GET method for multiple objects
        """
        response = authorized_client.get(self.URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert len(data) == 2

    @pytest.mark.like
    def test_get_user_likes_401(self, api_client):
        """
        Test of GET method as unauthorized user
        """
        response = api_client.get(self.URL)
        assert response.status_code == 401

        data = response.json()
        assert data is not None
        assert data.get("detail") == "Authentication credentials were not provided."


class TestGetLikesById:
    @pytest.mark.like
    def test_get_like_by_id(self, create_like, authorized_client, user_data):
        """
        Test of GET method for a like by its id
        """
        like_id = create_like.id
        URL = reverse("likes-detail", args=[like_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()

        assert data is not None
        assert data.get("id") == like_id
        assert data.get("created_at") is not None
        assert data.get("user") == user_data.id
        assert data.get("post") == create_like.post.id

    @pytest.mark.like
    def test_get_like_by_id_404(self, authorized_client):
        """
        Test of GET method for a like by its id.
        Returns error 404.
        """
        URL = reverse("likes-detail", args=[999])
        response = authorized_client.get(URL)
        assert response.status_code == 404

        data = response.json()
        assert data is not None
        assert data.get("detail") == 'No Like matches the given query.'

    @pytest.mark.like
    def test_get_like_by_id_401(self, api_client):
        """
        Test of GET method by unauthorized user
        """
        URL = reverse("likes-detail", args=[999])
        response = api_client.get(URL)
        assert response.status_code == 401

        data = response.json()
        assert data is not None
        assert data.get("detail") == "Authentication credentials were not provided."
