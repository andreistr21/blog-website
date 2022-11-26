from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def dave(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    view_count = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    # Related name makes it easy to do ?reverse? search
    # With out a related name: tag_1.post_set.all()
    # With related name: tag_1.post.all()
    tags = models.ManyToManyField(Tag, blank=True, related_name="post")


class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200, null=True, blank=True)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="replies")
    
    
class Subscribe(models.Model):
    email = models.EmailField(max_length=200)
    date = models.DateTimeField(auto_now=True)
