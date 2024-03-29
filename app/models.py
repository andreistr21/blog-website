from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from tinymce import models as tinymce_models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = tinymce_models.HTMLField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="images/", default="images/no_image.jpg")
    view_count = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    # Related name makes it easy to do ?reverse? search
    # With out a related name: tag_1.post_set.all()
    # With related name: tag_1.post.all()
    tags = models.ManyToManyField(Tag, related_name="post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="blog_post", blank=True)
    bookmarks = models.ManyToManyField(User, related_name="bookmarks", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    def __str__(self) -> str:
        return self.content


class Subscribe(models.Model):
    email = models.EmailField(max_length=200)
    date = models.DateTimeField(auto_now=True)


class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    about = models.TextField()

    def __str__(self) -> str:
        return self.title
