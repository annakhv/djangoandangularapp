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
from django.contrib.auth.models import User
from django.db.models import Q


@token_req
@csrf_exempt
def askQuestion_view(request, username):
    print("hello homee")
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    questionText=body['questionText']
    user=User.objects.get(username=username)
    if questionText != "":
       addQuestion=question.objects.create(user=user, userQuestion=questionText)
       print(addQuestion)
       return JsonResponse({"res" : True}) 
    else:
        return JsonResponse({"res" : False})
   

@token_req
@csrf_exempt
def getQuestions_view(request, username):
    print("getquestions")
    questionDict={}
    user=profile.objects.get(user__username=username)
    result=user.following.all()
    usernames=result.values_list('user__username', flat=True)
    questions=question.objects.filter(Q(user__username__in=usernames) | Q(user__username=username))
    print(questions)
    if questions:
        results=questions.filter().values('user__username', 'user__first_name', 'user__last_name', 'userQuestion', 'id').order_by('date')
        for item in results:
           questionDict[item['userQuestion']]=[item['user__first_name'], item['user__last_name'], item['user__username'], item['id']]
        jsona=json.dumps(questionDict)   
        return JsonResponse({"res" : True, 'json':jsona})
    else:
        return JsonResponse({"res" : False})


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