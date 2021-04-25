from django.shortcuts import render
from django.shortcuts import render
from datetime import datetime
import sys
sys.path.append(".")
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from home.models import question, answer, comment
from accounts.views import token_req
from accounts.models import profile
from django.contrib.auth.models import User
from django.db.models import Q



@token_req
@csrf_exempt
def personalActivity_view(request, username):
    user=User.objects.get(username=username)
    questions=user.allQuestions.all()
    infoDict={}
    infoList=[]
    _questions=questions.filter().values('date', 'userQuestion', 'id').order_by('date')
    for question in _questions:
        infoDict['question']=question['userQuestion']
        infoDict['id']=question['id']
        if question['date'] != None:
            date=question['date'].strftime("%m/%d/%Y, %H:%M:%S")
            infoDict['date']=date
        else:
            infoDict['date']=""
        infoList.append(infoDict)
        infoDict={}   
    answers=user.answers.all()
    _answers=answers.filter().values('date', 'userAnswer', "whichQuestion__userQuestion", 'id').order_by('date')
    for answer in _answers:
        infoDict['answer']=answer['userAnswer']
        infoDict['id']=answer['id']
        infoDict['toQuestion']=answer['whichQuestion__userQuestion']
        if answer['date'] != None:
            date=answer['date'].strftime("%m/%d/%Y, %H:%M:%S")
            infoDict['date']=date
        else:
            infoDict['date']=""
        infoList.append(infoDict)
        infoDict={} 
    comments=user.comments.all()
    _comments=comments.filter().values('date', 'userComment', "whichAnswer__userAnswer", "whichAnswer__whichQuestion__userQuestion", 'id').order_by('date')
    for comment in _comments:
        infoDict['comment']=comment['userComment']
        infoDict['id']=comment['id']
        infoDict['toAnswer']=comment["whichAnswer__userAnswer"]
        infoDict['ofQuestion']=comment["whichAnswer__whichQuestion__userQuestion"]
        if comment['date'] != None:
            date=comment['date'].strftime("%m/%d/%Y, %H:%M:%S")
            infoDict['date']=date
        else:
            infoDict['date']=""
        infoList.append(infoDict)
        infoDict={} 
    infoList=sorted(infoList, key=lambda item: item['date'],reverse=True)
    jsona=json.dumps(infoList)
    return JsonResponse({"res":True, "json": jsona})