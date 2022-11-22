from unicodedata import name
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200 ,unique=True)
    
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
    image = models.ImageField(null=True, blank=True, upload_to="imaages/")
    
    # Related name makes it easy to do ?reverse? search
    # With out a related name: tag_1.post_set.all()
    # With related nane: tag_1.post.all()
    tags = models.ManyToManyField(Tag, blank=True, related_name="post")
