from django.shortcuts import render, redirect, get_list_or_404
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from backend.apps.posts.models import Post
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from backend.apps.posts.forms import PostForm
from django.http import JsonResponse
import json

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


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return User.objects.filter(username__icontains=query).exclude(id=self.request.user.id)

        return User.objects.none()  # Not to show evety user at the start

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding PostForm
        context["post_form"] = PostForm()

        for user in context['results']:
            user.is_following = user.followers.filter(follower=self.request.user).exists()

        return context


@login_required
def add_bio(request):

    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    data = json.loads(request.body)
    bio = data.get("bio")

    user_profile = request.user.profile

    user_profile.bio = bio
    user_profile.save()

    return JsonResponse({"success": "bio successfully updated"})


@login_required
def update_photo(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    file = request.FILES.get("profile_picture")
    
    if not file:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    profile = request.user.profile
    profile.profile_picture = file
    profile.save()
    
    return JsonResponse({
        "success": "Photo successfully updated",
        "new_url": profile.profile_picture.url
        })