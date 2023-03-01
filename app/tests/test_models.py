from django.test import TestCase
from django.contrib.auth.models import User


from app.models import Tag
from app.models import Post


class TagModelTest(TestCase):
    def setUp(self):
        Tag.objects.create(name="Name of the tag", description="Test tag")

    def test_name_value(self):
        tag = Tag.objects.all().first()
        tag_name_val = tag.name
        self.assertEqual(tag_name_val, "Name of the tag")

    def test_desc_value(self):
        tag = Tag.objects.all().first()
        tag_desc_val = tag.description
        self.assertEqual(tag_desc_val, "Test tag")

    def test_returned_val(self):
        """Testing default string return value for the object"""
        tag = Tag.objects.all().first()
        self.assertEqual(str(tag), tag.name)


class PostModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="test_user", password="test_pass")
        tag = Tag.objects.create(name="Test tag", description="Test tag")
        post = Post(title="New post", content="<p>Content</p>", author=user)
        post.save()
        post.tags.add(tag)

    def test_name_val(self):
        post = Post.objects.first()
        post_title = post.title
        self.assertEqual(post_title, "New post")

    def test_content_val(self):
        post = Post.objects.first()
        post_content = post.content
        self.assertEqual(post_content, "<p>Content</p>")
        
    def test_slug_val(self):
        post = Post.objects.first()
        post_slug = post.slug
        self.assertEqual(post_slug, "new-post")

    def test_tag_existing(self):
        post = Post.objects.first()
        is_tag_exists = post.tags.exists()
        self.assertTrue(is_tag_exists)

    def test_post_cascade_delete(self):
        """Checks if the post will be deleted after the author is deleted."""
        post = Post.objects.first()
        post.author.delete()
        is_exists = Post.objects.all().exists()
        self.assertFalse(is_exists)
