from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from app.models import Post, WebsiteMeta, Subscribe


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_of_posts = 10
        for post_id in range(num_of_posts):
            Post.objects.create(title=f"Post#{post_id}", content=f"Content post {post_id}")

        WebsiteMeta.objects.create(
            title="The Super Blog", description="This is the best blog website", about="Some text"
        )

    def test_index_page_response_status(self):
        url = reverse("index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        
        
    def test_index_form_post(self):
        url = reverse("index")
        self.client.post(url, {"email": "test_email@gmail.com"})
        
        is_exists = Subscribe.objects.exists()
        self.assertTrue(is_exists)
        
        
class BookmarksViewTest(TestCase):
    def test_logged_user_access(self):
        url = reverse("my_bookmarks")
        credentials = {"username": "Test_user", "password": "test_pass"}
        User.objects.create_user(**credentials)
        self.client.login(**credentials)
        resp = self.client.get(url)
        
        resp_code = resp.status_code
        self.assertEqual(resp_code, 200)
        
        
    def test_anonymous_user_access(self):
        url = reverse("my_bookmarks")
        resp = self.client.get(url)
        
        resp_code = resp.status_code
        self.assertEqual(resp_code, 302)