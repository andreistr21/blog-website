from django.shortcuts import render
from django.shortcuts import redirect

from app.models import Comments, Post
from app.forms import CommentForm


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by("-view_count")[0:3]
    recent_posts = Post.objects.all().order_by("-last_updated")[0:3]
    context = {"posts": posts, "top_posts": top_posts, "recent_posts": recent_posts}

    return render(request, "app/index.html", context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if parent_comment_id := request.POST.get("parent"):
                parent_comment_obj = Comments.objects.get(id=parent_comment_id)
                if parent_comment_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_comment_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return redirect("post_page", slug=slug)

            else:
                comment = comment_form.save(commit=False)
                post_id = request.POST.get("post_id")
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return redirect("post_page", slug=slug)

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()

    context = {"post": post, "form": form, "comments": comments}

    return render(request, "app/post.html", context)
