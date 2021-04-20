from django.contrib import admin
from django.urls import path
from home import views




urlpatterns = [
     path('askQuestion', views.askQuestion_view, name="askQuestion"),
     path('answerQuestion', views.answerQuestion_view, name="answerQuestion"),
     path('addComment', views.addComment_view, name="addComment"),
     path('getQuestions', views.getQuestions_view, name="getQuestions"),
     path('getAnswersAndComments', views.getAnswersAndComments_view, name="getAnswersAndComments")
]