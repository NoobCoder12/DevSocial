import pytest
from django.urls import reverse


class TestPostPosts:
    """
    Class for tests of /posts/ endpoint
    """
    URL = reverse('posts-list')  # show_urls will show all url names
    POST_DATA = {
            "title": "Random title",
            "body": "Random body of a post"
        }
    
    @pytest.mark.posts
    def test_posts(self, authorized_client):
        """
        Test for post creation
        """
        # DRF automatically sends data is mulipart/form-data, not JSON
        response = authorized_client.post(self.URL, data=self.POST_DATA, format='json')
        assert response.status_code == 201
        data = response.json()
        assert data.get("message") == "Post created"

    @pytest.mark.posts
    def test_post_missing_title(self, authorized_client):
        """
        Test of posting with missing title
        """
        post = {
            "title": "",
            "body": "Random body of a post"
        }

        response = authorized_client.post(self.URL, data=post, format='json')
        assert response.status_code == 400

        response_data = response.json()
        assert response_data is not None
        assert response_data.get("title") == ['This field may not be blank.']

    @pytest.mark.posts
    def test_post_missing_body(self, authorized_client):
        """
        Test of posting with missing body
        """
        post = {
            "title": "Some title",
            "body": ""
        }

        response = authorized_client.post(self.URL, data=post, format='json')
        assert response.status_code == 400

        response_data = response.json()
        assert response_data is not None
        assert response_data.get("body") == ['This field may not be blank.']

    @pytest.mark.posts
    def test_post_unauthorized(self, api_client):
        """
        Test of posting as unathorized user
        """
        response = api_client.post(self.URL, data=self.POST_DATA, format='json')
        assert response.status_code == 401
        response_data = response.json()

        assert response_data is not None
        assert response_data.get("detail") == 'Authentication credentials were not provided.'


class TestGetPosts:
    URL = reverse('posts-list')

    @pytest.fixture
    def created_two_posts(self, authorized_client):
        """
        Creating post as a fixture
        """
        post1 = {
            "title": "Random title",
            "body": "Random body of a post"
        }

        post2 = {
            "title": "Definetely not random",
            "body": "Some story"
        }

        # DRF automatically sends data is mulipart/form-data, not JSON
        authorized_client.post(self.URL, data=post1, format='json')
        authorized_client.post(self.URL, data=post2, format='json')

        return post1, post2

    @pytest.mark.posts
    def test_get_posts(self, authorized_client, created_two_posts):
        post1, post2 = created_two_posts

        response = authorized_client.get(self.URL)
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 2

        post1_check, post2_check = response_data

        assert post1_check is not None
        assert post1_check.get("title") == post1.get("title")
        assert post1_check.get("body") == post1.get("body")

        assert post2_check is not None
        assert post2_check.get("title") == post2.get("title")
        assert post2_check.get("body") == post2.get("body")

    @pytest.mark.posts
    def test_get_unauthorized(self, api_client):
        """
        Get posts as unauthorized user
        """
        response = api_client.get(self.URL)
        assert response.status_code == 401
        response_data = response.json()

        assert response_data is not None
        assert response_data.get("detail") == 'Authentication credentials were not provided.'

    @pytest.mark.posts
    def test_get_empty(self, authorized_client):
        response = authorized_client.get(self.URL)
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 0


class TestGetIdPosts:
    """
    Tests for getting a post by its ID
    """
    URL = reverse('posts-list')

    @pytest.fixture
    def create_post(self, authorized_client):
        """
        Creating single post as a fixture
        """
        post = {
            "title": "Hello recruiter",
            "body": "I hope you are satisfied with what you see"
        }

        # DRF automatically sends data is mulipart/form-data, not JSON
        response = authorized_client.post(self.URL, data=post, format='json')

        return post, response.json()

    @pytest.mark.posts
    def test_get_post(self, create_post, authorized_client):
        """
        Get post by ID
        """
        post_body, post_id_part = create_post
        post_id = post_id_part.get("id")
        GET_URL = reverse('posts-detail', args=[post_id])

        response = authorized_client.get(GET_URL)
        assert response.status_code == 200

        post_data = response.json()
        assert post_data is not None
        assert create_post[1].get("id") == post_data.get("id")     # Otherwise post would not be found
        assert post_body.get("title") == post_data.get("title")
        assert post_body.get("body") == post_data.get("body")

    @pytest.mark.posts
    def test_get_post_404(self, authorized_client):
        """
        Get non existing post
        """
        post_id = 999
        GET_URL = reverse('posts-detail', args=[post_id])

        response = authorized_client.get(GET_URL)
        assert response.status_code == 404

        post_data = response.json()
        assert post_data is not None
        assert post_data.get("detail") == 'No Post matches the given query.'

    @pytest.mark.posts
    def test_get_post_401(self, api_client):
        """
        Get post as unauthorized user
        """
        post_id = 999
        GET_URL = reverse('posts-detail', args=[post_id])

        response = api_client.get(GET_URL)
        assert response.status_code == 401

        post_data = response.json()
        assert post_data is not None
        assert post_data.get("detail") == 'Authentication credentials were not provided.'

# class TestPutIdPost
# class TestPatchIdPost
# class TestDeleteIdPost