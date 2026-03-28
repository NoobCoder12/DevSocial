import pytest
from django.urls import reverse


@pytest.fixture
def create_post(authorized_client):
    """
    Creating single post as a fixture
    """
    post = {
        "title": "Hello recruiter",
        "body": "I hope you are satisfied with what you see"
    }

    # DRF automatically sends data is mulipart/form-data, not JSON
    response = authorized_client.post(reverse('posts-list'), data=post, format='json')

    return post, response.json()


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


class TestPutIdPost:
    @pytest.mark.posts
    def test_put_post(self, create_post, authorized_client):
        """
        Test PUT method on a post
        """
        # Extracting all data from post
        post, post_info = create_post
        post_title = post.get("title")
        post_body = post.get("body")
        post_id = post_info.get("id")

        URL = reverse("posts-detail", args=[post_id])

        new_data = {
            "title": "Welcome from new title",
            "body": "And don't forget about me!"
        }

        response = authorized_client.put(URL, data=new_data, format='json')

        assert response.status_code == 200

        post_data = response.json()
        assert post_data is not None

        # Get new post data
        new_id = post_data.get("id")
        new_title = post_data.get("title")
        new_body = post_data.get("body")

        # Check if edited fields are saved
        assert new_id == post_id
        assert new_title != post_title
        assert new_body != post_body

    @pytest.mark.posts
    def test_put_missing_body(self, create_post, authorized_client):
        # Extracting all data from post
        post_info = create_post[1]
        post_id = post_info.get("id")

        URL = reverse("posts-detail", args=[post_id])

        new_data = {
            "title": "Welcome from new title"
        }

        response = authorized_client.put(URL, data=new_data, format='json')

        assert response.status_code == 400
        data = response.json()

        assert data is not None
        assert data.get("body") == ['This field is required.']

    @pytest.mark.posts
    def test_put_missing_title(self, create_post, authorized_client):
        # Extracting all data from post
        post_info = create_post[1]
        post_id = post_info.get("id")

        URL = reverse("posts-detail", args=[post_id])

        new_data = {
            "body": "And don't forget about me!"
        }

        response = authorized_client.put(URL, data=new_data, format='json')

        assert response.status_code == 400
        data = response.json()

        assert data is not None
        assert data.get("title") == ['This field is required.']

    @pytest.mark.posts
    def test_put_unauthorized(self, api_client):
        # Test on any post, just authentication needed
        URL = reverse("posts-detail", args=[1])

        new_data = {
            "title": "Welcome from new title",
            "body": "And don't forget about me!"
        }

        response = api_client.put(URL, data=new_data, format='json')

        assert response.status_code == 401
        data = response.json()

        assert data is not None
        assert data.get("detail") == 'Authentication credentials were not provided.'


class TestPatchIdPost:
    @pytest.mark.posts
    def test_patch_post_title(self, create_post, authorized_client):
        """
        Test PATCH method on a post
        """
        # Extracting all data from post
        post, post_info = create_post
        post_title = post.get("title")
        post_body = post.get("body")
        post_id = post_info.get("id")

        URL = reverse("posts-detail", args=[post_id])

        new_data = {
            "title": "Welcome from new title"
        }

        response = authorized_client.patch(URL, data=new_data, format='json')

        assert response.status_code == 200

        post_data = response.json()
        assert post_data is not None

        # Get new post data
        new_id = post_data.get("id")
        new_title = post_data.get("title")
        new_body = post_data.get("body")

        # Check if edited fields are saved
        assert new_id == post_id
        assert new_title != post_title
        assert new_body == post_body

    @pytest.mark.posts
    def test_patch_post_body(self, create_post, authorized_client):
        # Extracting all data from post
        post, post_info = create_post
        post_title = post.get("title")
        post_body = post.get("body")
        post_id = post_info.get("id")

        URL = reverse("posts-detail", args=[post_id])

        new_data = {
           "body": "And don't forget about me!"
        }

        response = authorized_client.patch(URL, data=new_data, format='json')

        assert response.status_code == 200

        post_data = response.json()
        assert post_data is not None

        # Get new post data
        new_id = post_data.get("id")
        new_title = post_data.get("title")
        new_body = post_data.get("body")

        # Check if edited fields are saved
        assert new_id == post_id
        assert new_title == post_title
        assert new_body != post_body

    @pytest.mark.posts
    def test_patch_post_unauthorized(self, api_client):
        # Extracting all data from post
        URL = reverse("posts-detail", args=[1])

        response = api_client.patch(URL, data={}, format='json')

        assert response.status_code == 401

        data = response.json()
        assert data is not None
        assert data.get("detail") == 'Authentication credentials were not provided.'

    @pytest.mark.posts
    def test_patch_post_404(self, authorized_client):
        URL = reverse("posts-detail", args=[999])

        response = authorized_client.patch(URL, data={}, format='json')

        assert response.status_code == 404

        data = response.json()
        assert data is not None
        assert data.get('detail') == 'No Post matches the given query.'


class TestDeleteIdPost:
    @pytest.mark.posts
    def test_delete_post(self, create_post, authorized_client):
        """"
        Test DELETE method on post
        """
        # Extracting all id from post
        post_info = create_post[1]
        post_id = post_info.get("id")

        URL = reverse("posts-detail", args=[post_id])

        response = authorized_client.delete(URL)

        assert response.status_code == 200

        data = response.json()
        assert data is not None
        assert data.get("message") == 'Post deleted'

    @pytest.mark.posts
    def test_delete_post_404(self, authorized_client):
        """"
        Test DELETE method on non existing post
        """

        URL = reverse("posts-detail", args=[999])

        response = authorized_client.delete(URL)

        assert response.status_code == 404

        data = response.json()
        assert data is not None
        assert data.get('detail') == 'No Post matches the given query.'

    @pytest.mark.posts
    def test_delete_authorization(self, api_client):
        """"
        Test DELETE method as non authenticated user
        """
        URL = reverse("posts-detail", args=[999])

        response = api_client.delete(URL)

        assert response.status_code == 401

        data = response.json()
        assert data is not None
        assert data.get('detail') == 'Authentication credentials were not provided.'
