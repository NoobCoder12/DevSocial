from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding PostForm
        context["post_form"] = PostForm()

        # Liked state for every post
        for post in context['posts']:
            # Creating a variable for bool
            post.user_liked = post.is_liked_by(user=self.request.user)

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        # Assign request.user to form instance
        form.instance.author = self.request.user
        messages.success(self.request, "Post added successfully")
        return super().form_valid(form)

    def get_success_url(self):
        # User is not redirected after posting in modal
        return self.request.META.get('HTTP_REFERER', reverse_lazy("posts:home"))



# @login_required
# def new_post(request):
#     if request.method == "POST":
#         post = PostForm(request.POST)
#         if post.is_valid():
#             new_post = post.save(commit=False)
#             new_post.author = request.user
#             new_post.save()
#             messages.success(request, "Post added successfully")
#             return redirect(request.META.get('HTTP_REFERER', '/'))
#         else:
#             messages.error(request, 'Please fill out visible fields')

