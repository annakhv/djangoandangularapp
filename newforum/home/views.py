from django.shortcuts import render
import datetime
import sys
import sys
sys.path.append(".")
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import question, answer, comment
from accounts.views import token_req
from accounts.models import profile


@token_req
@csrf_exempt
def askQuestion_view(request, username):
    print("hello homee")
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    question=body['question']
    user=User.objects.get(username=username)
    if question != "":
       question=question.objects.create(user=user, question=question)
       print(question)
       return JsonResponse({"res" : True}) 
    else:
        return JsonResponse({"res" : False})
   

@token_req
@csrf_exempt
def getQuestions_view(request, username):
    return JsonResponse({"res" : True})


@token_req
@csrf_exempt
def answerQuestion_view(request, username, question_id):

    return JsonResponse({"res" : True})


@token_req
@csrf_exempt
def getAnswersAndComments_view(request, username):

    return JsonResponse({"res" : True})


@token_req
@csrf_exempt
def addComment_view(request, username, answer_id):

    return JsonResponse({"res" : True})