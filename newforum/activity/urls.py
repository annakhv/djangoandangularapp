from django.contrib import admin
from django.urls import path
from activity import views

urlpatterns=[
  path('personalActivity/<username>', views.personalActivity_view, name="personalActivity")
]