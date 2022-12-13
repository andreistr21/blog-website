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
    path("new_post/", views.new_post_page, name="new-post"),
]
