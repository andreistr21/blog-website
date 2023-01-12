from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>", views.post_page, name="post_page"),
    path("tag/<slug:slug>", views.tag_page, name="tag_page"),
    path("author/<slug:slug>", views.author_page, name="author_page"),
    path("search/", views.search_posts, name="search"),
    path("about/", views.about_page, name="about"),
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(template_name="app/logout.html"), name="logout"),
    path("like-post/", views.like_post, name="like-post"),
    path("new-post/", views.new_post_page, name="new-post"),
    path("edit-post/<slug:slug>", views.edit_post_page, name="edit-post"),
    path("my-posts", views.my_posts_page, name="my_posts"),
    path("all-posts", views.all_posts_page, name="all_posts"),
    path("delete/<slug:slug>", views.delete_post, name="delete_post"),
    path("comment-delete/<int:id>", views.comment_delete_view, name="comment_delete"),
]
