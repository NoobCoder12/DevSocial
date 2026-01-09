from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from backend.apps.posts.models import Post
from .models import Like
from django.http import JsonResponse

# Create your views here.


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
