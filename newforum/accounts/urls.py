from django.contrib import admin
from django.urls import path
from accounts import views


urlpatterns = [
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout/<username>', views.logout_view, name="logout"),
    path('profile/<username>', views.profile_view, name="profile"),
    path('updateProfile/<username>', views.updateProfile_view, name="updateProfile"),
    path('addAndUpdateEdu/<username>/<id>', views.addAndUpdateEdu_view, name="addAndUpdateEdu"),
    path('addAndUpdateWork/<username>/<id>', views.addAndUpdateWork_view, name="addAndUpdateWork"),
    path('getEdu/<username>', views.getEdu_view, name="getEdu"),
    path('getWork/<username>', views.getWork_view, name="getWork"),
    path('search/<searchtext>', views.search_view, name="search"),
    path('followUser/<thisUsername>/<otherUsername>', views.followUser_view, name="followUser"),
    path('getFollowers/<thisUsername>', views.getFollowers_view, name="getFollowers"),
    path('getFollowing/<thisUsername>', views.getFollowing_view, name="getFollowing"),
    path('deleteEdu/<edu_id>', views.deleteEdu_view, name="deleteEdu"),
    path('deleteWork/<work_id>', views.deleteWork_view, name="deleteWork"),
    path('ifThisUsernameFollows/<thisUsername>/<otherUsername>', views.ifThisUsernameFollows_view, name="ifThisUsernameFollows")
]
