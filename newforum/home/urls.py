from django.contrib import admin
from django.urls import path
from home import views




urlpatterns = [
     path('askQuestion/<username>', views.askQuestion_view, name="askQuestion"),
     path('answerQuestion/<username>/<question_id>', views.answerQuestion_view, name="answerQuestion"),
     path('addComment/<username>/<answer_id>', views.addComment_view, name="addComment"),
     path('getQuestions/<username>', views.getQuestions_view, name="getQuestions"),
     path('getAnswersAndComments/<username>', views.getAnswersAndComments_view, name="getAnswersAndComments")
]