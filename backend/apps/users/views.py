from django.shortcuts import render, redirect, get_list_or_404
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from backend.apps.posts.models import Post

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user_data = login_form.get_user()
            login(request, user_data)
            next_url = request.POST.get('next')
            return redirect(next_url or 'posts:home')
    else:
        login_form = AuthenticationForm()

    next_url = request.GET.get('next', '')
    return render(request, 'users/login.html', {'login_form': login_form, 'next': next_url})


def create_user(request):
    user_form = CustomUserCreationForm()

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, "User created successfully")
            return redirect('posts:home')

    return render(request, 'users/create_user.html', {'user_form': user_form})


@login_required
def my_account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user).order_by("-date")
    return render(request, 'users/my_account.html', {"profile": profile, "posts": posts})


@login_required
def search_user(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, "users/search.html", {'results': results})