import pytest
from django.urls import reverse


class TestPostPosts:
    @pytest.mark.posts
    def test_posts(self, authorized_client):
        """
        Test for post creation
        """
        url = reverse('posts-list') # show_urls will show all url names
        post = {
            "title": "Random title",
            "body": "Random body of a post"
        }
        # DRF automatically sends data is mulipart/form-data, not JSON
        response = authorized_client.post(url, data=post, format='json')
        assert response.status_code == 201
        data = response.json()
        assert data.get("message") == "Post created"
