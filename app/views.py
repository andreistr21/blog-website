import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from app.forms import CommentForm, LoginForm, PostForm, SignupForm, SubscribeForm
from app.models import Comments, Post, Profile, Tag, WebsiteMeta


def is_user_anonymous(request):
    return not request.user.is_authenticated


def not_creator(request, post):
    return request.user.id != post.author.id


def like_post(request):
    if not request.POST:
        return HttpResponseNotFound()

    slug = request.POST.get("post_slug")
    post_obj = Post.objects.get(slug=slug)
    user = request.user

    if user.is_authenticated:
        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

    return redirect(post_page, slug=slug)


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by("-view_count")[:3]
    recent_posts = Post.objects.all().order_by("-last_updated")[:3]
    featured_post = Post.objects.filter(is_featured=True).first()
    subscribe_form = SubscribeForm()
    subscribe_successful = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = "Subscribed Successfully"
            subscribe_form = SubscribeForm()

    context = {
        "posts": posts,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "subscribe_form": subscribe_form,
        "subscribe_successful": subscribe_successful,
        "featured_post": featured_post,
        "website_info": website_info,
    }
    return render(request, "app/index.html", context)


def add_comment(request, post):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)

        if parent_comment_id := request.POST.get("parent"):
            if parent_comment_obj := get_object_or_404(Comments, id=parent_comment_id):
                comment.parent = parent_comment_obj

        comment.post = post
        author = get_object_or_404(User, id=request.POST.get("user_id"))
        comment.author = author
        comment.save()
        return True


def update_view_counter(post):
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()


def post_page(request, slug):  # sourcery skip: extract-duplicate-method
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.POST and add_comment(request, post):
        return redirect("post_page", slug=slug)

    update_view_counter(post)

    context = {"post": post, "form": form, "comments": comments}
    return render(request, "app/post.html", context)


def tag_page(request, slug):
    tags = Tag.objects.all()
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-view_count")[:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-last_updated")[:3]

    context = {"tag": tag, "tags": tags, "top_posts": top_posts, "recent_posts": recent_posts}
    return render(request, "app/tag.html", context)


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)

    top_posts = Post.objects.filter(author=profile.user).order_by("-view_count")[:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by("-last_updated")[:3]
    top_authors = User.objects.annotate(number=Count("post")).order_by("number")

    context = {"profile": profile, "top_posts": top_posts, "recent_posts": recent_posts, "top_authors": top_authors}
    return render(request, "app/author.html", context)


def search_posts(request):
    posts = ()
    if search_query := (request.GET.get("q") or ""):
        posts = Post.objects.filter(title__icontains=search_query)

    context = {"posts": posts, "search_query": search_query}
    return render(request, "app/search.html", context)


def about_page(request):
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {"website_info": website_info}
    return render(request, "app/about.html", context)


def login_page(request):  # sourcery skip: use-named-expression
    form = LoginForm()
    logging_failed = False

    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect("my_posts")
            else:
                logging_failed = True

    context = {"form": form, "is_authenticated": request.user.is_authenticated, "logging_failed": logging_failed}
    return render(request, "app/login.html", context)


def signup_page(request):
    form = SignupForm()

    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
            )
            login(request, user)
            return redirect("my_posts")

    context = {"form": form, "is_authenticated": request.user.is_authenticated}
    return render(request, "app/signup.html", context)


def new_post_page(request):
    if is_user_anonymous(request):
        return HttpResponseForbidden()

    new_post_form = PostForm()

    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.author = request.user
            post_obj.save()
            return redirect("post_page", post_obj.slug)

    context = {"form": new_post_form}
    return render(request, "app/new_post.html", context)


def edit_post_page(request, slug):
    post_obj = get_object_or_404(Post, slug=slug)

    if is_user_anonymous(request) or not_creator(request, post_obj):
        return HttpResponseForbidden()

    image_url = request.build_absolute_uri(post_obj.image.url)
    post_form = PostForm(instance=post_obj)

    if request.POST and not request.POST.get("action"):
        post_form = PostForm(request.POST, request.FILES, instance=post_obj)
        if post_form.is_valid():
            post_obj = post_form.save()
            return redirect("post_page", post_obj.slug)

    context = {"post_form": post_form, "image_url": image_url}
    return render(request, "app/edit-post.html", context)


def my_posts_page(request):
    if is_user_anonymous(request):
        return HttpResponseForbidden()

    author_id = request.user.id
    author_posts = Post.objects.filter(author__id=author_id).order_by("last_updated")

    context = {"author_posts": author_posts}
    return render(request, "app/my_posts.html", context)


def delete_post(request, slug):
    post_obj = get_object_or_404(Post, slug=slug)

    if is_user_anonymous(request) or not_creator(request, post_obj):
        return HttpResponseForbidden()

    if request.POST and request.POST.get("delete"):
        post_obj.delete()
        return redirect("my_posts")

    context = {"post_obj": post_obj}
    return render(request, "app/delete.html", context)


def comment_delete_view(_, id):
    comment = get_object_or_404(Comments, id=id)
    post = get_object_or_404(Post, id=comment.post.id)
    comment.delete()
    return redirect("post_page", slug=post.slug)
