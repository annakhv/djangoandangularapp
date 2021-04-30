from django.contrib import admin
from django.urls import path
from home import views




urlpatterns = [
     path('askQuestion/<username>', views.askQuestion_view, name="askQuestion"),
     path('answerQuestion/<username>/<question_id>', views.answerQuestion_view, name="answerQuestion"),
     path('addComment/<username>/<answer_id>', views.addComment_view, name="addComment"),
     path('getQuestions/<username>', views.getQuestions_view, name="getQuestions"),
     path('getAnswers/<username>', views.getAnswers_view, name="getAnswers"),
     path('getComment/<username>/<answer_id>', views.getComment_view, name="getComment"),
     path('upVoteAnswer/<username>/<answer_id>', views.upVoteAnswer_view, name='upVoteAnswer')
]