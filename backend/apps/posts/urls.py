from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('new-post/', views.new_post, name='new-post'),
]