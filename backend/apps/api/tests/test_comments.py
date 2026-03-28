import pytest
from django.urls import reverse
from model_bakery import baker
from backend.apps.posts.models import Post


@pytest.fixture
def create_comment(create_post, user_data):
    """
    Fixture for one post
    """
    post_id = create_post[1].get("id")
    post = Post.objects.get(id=post_id)
    comment = baker.make(
        'interactions.Comment',
        user=user_data,
        post=post,
        body='This is comment body'
    )
    return comment


@pytest.fixture
def create_two_comments(create_post, user_data):
    """
    Fixture for creation of 2 comments
    """
    post_id = create_post[1].get("id")
    post = Post.objects.get(id=post_id)
    comment = baker.make(
        'interactions.Comment',
        user=user_data,
        post=post,
        body='This is comment body'
    )
    comment2 = baker.make(
        'interactions.Comment',
        user=user_data,
        post=post,
        body='And the second one'
    )
    return comment, comment2


class TestAllComments:
    URL = reverse("comments-list")

    @pytest.mark.comments
    def test_get_my_comments(self, create_comment, authorized_client, user_data):
        """
        Test of GET method for comment of current user
        """
        response = authorized_client.get(self.URL)

        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 1
        data = response.json()[0]

        # Get each data from comment
        assert data.get("body") == 'This is comment body'
        assert data.get("user") == user_data.id
        assert data.get("post") == create_comment.post.id
        assert data.get("created_at") is not None
        assert data.get("id") == create_comment.id

    @pytest.mark.comments
    def test_get_my_two_comments(
        self,
        create_two_comments,
        authorized_client,
        user_data
    ):
        """
        Test of GET method for 2 comments of current user
        """
        response = authorized_client.get(self.URL)

        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 2

    @pytest.mark.comments
    def test_get_comments_401(
        self,
        api_client
    ):
        """
        Test of GET method for unauthorized user
        """
        response = api_client.get(self.URL)
        assert response.status_code == 401
        data = response.json()
        assert data is not None
        assert data.get("detail") == "Authentication credentials were not provided."


class TestCommentById:
    @pytest.mark.comments
    def test_get_comment_by_id(self, create_two_comments, authorized_client, user_data):
        """
        Test of GET comment by id
        """
        comment = create_two_comments[1]
        comment_id = comment.id
        URL = reverse("comments-detail", args=[comment_id])
        response = authorized_client.get(URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None

        # Check each field
        assert data.get("id") == comment_id
        assert data.get("body") == comment.body
        assert data.get("created_at") is not None
        assert data.get("user") == user_data.id
        assert data.get("post") == comment.post.id

    @pytest.mark.comments
    def test_get_comments_by_id_404(self, authorized_client):
        """
        Test of GET comment by wrong id
        """
        URL = reverse("comments-detail", args=[999])
        response = authorized_client.get(URL)
        assert response.status_code == 404

        data = response.json()
        assert data is not None

        assert data.get("detail") == 'No Comment matches the given query.'

    @pytest.mark.comments
    def test_get_comments_by_id_401(self, api_client):
        """
        Test of GET comment by unauthorized user
        """
        URL = reverse("comments-detail", args=[1])
        response = api_client.get(URL)
        assert response.status_code == 401

        data = response.json()
        assert data is not None

        assert data.get("detail") == "Authentication credentials were not provided."
