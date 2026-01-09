from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'interactions'

urlpatterns = [
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
]