from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from backend.apps.posts.models import Post
from .models import Like, Comment
from django.http import JsonResponse
import json
from django.template.loader import render_to_string

# Create your views here.

# Likes
@login_required
def toggle_like(request, slug):

    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    post = get_object_or_404(Post, slug=slug)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })


# Comments
@login_required
def add_comment(request, slug):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    post = get_object_or_404(Post, slug=slug)
    user = request.user

    data = json.loads(request.body)
    body = data.get("body")

    if body:
        comment = Comment.objects.create(user=user, post=post, body=body)

        # Render html for comment to string
        html = render_to_string('posts/partials/comment_item.html',
                                {'comment': comment},
                                request=request)

        # Sending HTML in JSON package
        return JsonResponse({"status": "success", "html": html})

    return JsonResponse({"status": "error"}, status=400)
