from django.shortcuts import render
from datetime import datetime
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
import random

@token_req
@csrf_exempt
def askQuestion_view(request, username):
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    questionText=body['questionText']
    user=User.objects.get(username=username)
    if questionText != "":
       addQuestion=question.objects.create(user=user, userQuestion=questionText)
       return JsonResponse({"res" : True}) 
    else:
        return JsonResponse({"res" : False})
   

@token_req
@csrf_exempt
def getQuestions_view(request, username):
    print("getquestions")
    user=profile.objects.get(user__username=username)
    result=user.following.all()
    usernames=result.values_list('user__username', flat=True)
    questions=question.objects.filter(Q(user__username__in=usernames) | Q(user__username=username))
    if questions:
        results=questions.filter().values('user__username', 'user__first_name', 'user__last_name', 'userQuestion', 'id').order_by('-date')
        jsona=processQuestions(results)   
        return JsonResponse({"res" : True, 'json':jsona})
    else:
        lastObjId=question.objects.latest('id').id
        randomList=random.sample(range(1,lastObjId), 20)
        questions=question.objects.filter(id__in=randomList)
        results=questions.filter().values('user__username', 'user__first_name', 'user__last_name', 'userQuestion', 'id').order_by('-date')
        jsona=processQuestions(results)
        return JsonResponse({"res" : True, 'json':jsona})


@token_req
@csrf_exempt
def answerQuestion_view(request, username, question_id):
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    answerToQuestion=body['answerText']
    if answerToQuestion != "":
       user=User.objects.get(username=username)
       questionToAnswer=question.objects.get(id=question_id)
       addanswer=answer.objects.create(user=user, whichQuestion=questionToAnswer, userAnswer=answerToQuestion )
       message="answer has been added successfuly"
       return JsonResponse({"res" : True, 'message': message})
    else:
       message="try again"
       return JsonResponse({"res" : False, 'message': message})

@token_req
@csrf_exempt
def getAnswers_view(request, username):
    user=profile.objects.get(user__username=username)
    result=user.following.all()
    usernames=result.values_list('user__username', flat=True)
    answers=answer.objects.filter(Q(user__username__in=usernames) | Q(user__username=username))
    results=answers.filter().values('user__username', 'user__first_name', 'user__last_name', 'whichQuestion' ,'whichQuestion__userQuestion','userAnswer' , 'id', 'date').order_by('date')
    if results:
     #  jsona=json.dumps(resultList)
       resultList=processAnswer(results, username)
       return JsonResponse({"res" : True, 'json':resultList })
    else:
       lastObjId=answer.objects.latest('id').id
       randomList=random.sample(range(1,lastObjId), 20)
       answers=answer.objects.filter(id__in=randomList)
       results=answers.filter().values('user__username', 'user__first_name', 'user__last_name', 'whichQuestion' ,'whichQuestion__userQuestion','userAnswer' , 'id', 'date').order_by('date')
       resultList=processAnswer(results, username)
       return JsonResponse({"res":True, 'json':resultList})

@token_req
@csrf_exempt
def addComment_view(request, username, answer_id):
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    print(body)
    commentToAnswer=body['commentText']
    if commentToAnswer != "":
       user=User.objects.get(username=username)
       whichAnswer=answer.objects.get(id=answer_id)
       addComment=comment.objects.create(user=user, whichAnswer=whichAnswer, userComment=commentToAnswer )
       message="answer has been added successfuly"
       return JsonResponse({"res" : True, 'message': message})
    else:
       message="try again"
       return JsonResponse({"res" : False, 'message': message})
   
@token_req
@csrf_exempt
def getComment_view(request,  username, answer_id):
   commentDict={}
   resultList=[]
   answerToComment=answer.objects.get(id=answer_id)
   comments=answerToComment.allComments.all()
   print(comments)
   results=comments.filter().values('user__first_name', 'user__last_name', 'userComment', 'date').order_by('date')
   if results:
      for result in results:
          commentDict['firstname']=result['user__first_name']
          commentDict['lastname']=result['user__last_name']
          commentDict['comment']=result['userComment']
          if result['date'] != None:
             date=result['date'].strftime("%m/%d/%Y, %H:%M:%S")
             commentDict['date']=date
          resultList.insert(0, commentDict)
          commentDict={}
      jsona=json.dumps(resultList)
      return JsonResponse({"res" : True, "json":jsona})
   else:
      return JsonResponse({"res" : False, "message":"no comment has been found" })




@token_req
@csrf_exempt
def thisQuestionAnswers_view(request, questionId):
   dic={}
   dicQuestion={}
   List=[]
   theQuestion=question.objects.get(id=questionId)
   ques=theQuestion.userQuestion
   quesDate=theQuestion.date.strftime("%m/%d/%Y, %H:%M:%S") if theQuestion.date is not None else ""
   print(quesDate)
   firstname=theQuestion.user.first_name
   lastname=theQuestion.user.last_name
   answers=theQuestion.allAnswers.all()
   dicQuestion['question']=ques
   dicQuestion['date']=quesDate
   dicQuestion['firstname']=firstname
   dicQuestion['lastname']=lastname
   results=answers.filter().values('userAnswer', 'date', 'user__first_name', 'user__last_name').order_by('-date')
   for result in results:
       dic["answer"]=result['userAnswer']
       if result['date'] != None:
             date=result['date'].strftime("%m/%d/%Y, %H:%M:%S")
             dic['date']=date
       dic["firstname"]=result["user__first_name"]
       dic['lastname']=result["user__last_name"]
       List.append(dic)
       dic={}
   jsona=json.dumps(List)
   return JsonResponse({"res" : True, "json":jsona, "questionInfo": dicQuestion})








@token_req
@csrf_exempt
def upVoteAnswer_view(request,  username, answer_id):     
    answerToUpVote=answer.objects.get(id=answer_id)
    user=User.objects.get(username=username)
    upVotes=answerToUpVote.upVotes.all()
    print(upVotes)
    if upVotes.filter(username=username).exists():
       answerToUpVote.upVotes.remove(user)
    else:
       print("add")
       answerToUpVote.upVotes.add(user)
    return JsonResponse({"res" : True})

def processQuestions(results):
    questionDict={}
    for item in results:
           questionDict[item['userQuestion']]=[item['user__first_name'], item['user__last_name'], item['user__username'], item['id']]
    jsona=json.dumps(questionDict)  
    return jsona
def processAnswer(results, username):
       resultList=[]
       answerDict={}
       for result in results:
           answerDict['username']=result['user__username']
           answerDict['firstname']=result['user__first_name']
           answerDict['lastname']=result['user__last_name']
           answerDict['questionId']=result['whichQuestion']
           answerDict['question']=result['whichQuestion__userQuestion']
           answerDict['answerId']=result['id']
           upVotes=answer.objects.get(id=result['id']).upVotes.all()
           if upVotes.filter(username=username).exists():
              answerDict['thisUserUpVotedAnswer']=True
           else:
              answerDict['thisUserUpVotedAnswer']=False
           answerDict['upVotes']=upVotes.count()
           answerDict['answer']=result['userAnswer']
           if result['date'] !=  None:
               date=result['date'].strftime("%m/%d/%Y, %H:%M:%S")
               answerDict['date']=date
           resultList.insert(0, answerDict)
           answerDict={}
       resultList=sorted(resultList, key=lambda item: item['upVotes'], reverse=True)
       return resultList