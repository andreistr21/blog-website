from django.contrib import admin

from app.models import Comments, Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
