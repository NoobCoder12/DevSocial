from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
   path('', views.login_view, name='login'),
   path('create/', views.create_user, name='create-user'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('my-account/', views.my_account, name='my-account'),
   path('search-user/', views.UsersListView.as_view(), name='search-user'),
]