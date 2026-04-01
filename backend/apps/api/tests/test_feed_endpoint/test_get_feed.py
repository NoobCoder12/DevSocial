import pytest
from django.urls import reverse
from backend.apps.posts.models import Post


class TestGetFeed:
    URL = reverse('feed-list')

    @pytest.mark.feed
    def test_get_feed(
        self,
        posts_created_by_followed_user,
        authorized_client,
        second_user_data
    ):
        """
        Test of GET method for current user feed
        """
        response = authorized_client.get(self.URL)
        assert response.status_code == 200
        data = response.json()
        assert data is not None

        # Split data for 2 posts
        post1, post2 = data

        assert post1.get("id") != post2.get("id")

        # Get values from first post
        assert isinstance(post1.get("id"), int)
        assert isinstance(post1.get("likes_count"), int)
        assert isinstance(post1.get("comments_count"), int)
        assert post1.get("title") == 'First test post'
        assert post1.get("slug") is not None
        assert post1.get("body") == 'This is first post for feed test'
        assert post1.get("date") is not None
        assert post1.get("author") == second_user_data.id

        # Get values from second post
        assert isinstance(post2.get("id"), int)
        assert isinstance(post2.get("likes_count"), int)
        assert isinstance(post2.get("comments_count"), int)
        assert post2.get("title") == 'Dear Recruiters'
        assert post2.get("slug") is not None
        assert post2.get("body") == 'I hope you got to this point and the second test post is visible for you'
        assert post2.get("date") is not None
        assert post2.get("author") == second_user_data.id

    @pytest.mark.feed
    def test_get_feed_no_follow(
        self,
        authorized_client,
        posts_created_by_followed_user,
        third_user_post
    ):
        """
        Test of GET method for feed of non-followed user
        """
        # Check the quantity of all posts
        posts = Post.objects.all()
        assert len(posts) == 3

        response = authorized_client.get(self.URL)
        assert response.status_code == 200
        data = response.json()

        # Check the number of visible on feed posts
        assert len(data) == 2

    @pytest.mark.feed
    def test_get_feed_401(self, api_client):
        """
        Test of GET method by unauthorized user
        """     
        response = api_client.get(self.URL)
        assert response.status_code == 401
        response_data = response.json()

        assert response_data is not None
        assert response_data.get("detail") == 'Authentication credentials were not provided.'