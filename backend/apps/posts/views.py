from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    form = PostForm()
    posts = Post.objects.filter(author=request.user)
    
    for post in posts:
        post.user_liked = post.likes.filter(user=request.user).exists()
        
    return render(request, 'posts/home.html', {'post_form': form, 'posts': posts})


@login_required
def new_post(request):
    if request.method == "POST":
        post = PostForm(request.POST)
        if post.is_valid():
            new_post = post.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, "Post added successfully")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Please fill out visible fields')

