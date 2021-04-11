from django.contrib import admin
from django.urls import path
from accounts import views


urlpatterns = [
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('profile/<username>', views.profile_view, name="profile"),
    path('updateProfile/<username>', views.updateProfile_view, name="updateProfile"),
  
]
