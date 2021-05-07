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
from .models import message


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




@token_req
@csrf_exempt
def activeUsers_view(request, username):
    userList=[]
    userDic={}
    thisUserProfile=profile.objects.get(user__username=username)
    allFollowing=thisUserProfile.following.all()
    results=allFollowing.filter(is_active=True).values('user__username', 'user__first_name', 'user__last_name')
    if results:
       for result in results:
           userDic['username']=result['user__username']
           userDic['firstname']=result['user__first_name']
           userDic['lastname']=result['user__last_name']
           userList.append(userDic)
           userDic={}
       print(userList)
       jsona=json.dumps(userList)
       return JsonResponse({"res":True, "json": jsona})
    else:
       return JsonResponse({"res":False, "message": "no user that you follow is actve right now" })




@token_req
@csrf_exempt
def getSentMessages_view(request, username):
    resultList=[]
    answerDict={}
    user=User.objects.get(username=username)
    allMessages=user.messages.all()
    results=allMessages.filter(deleteFromSender=False).values('id', 'toUser__first_name', 'toUser__last_name', 'title', 'date').order_by('-date')
    if results:
       for result in results:
           answerDict['id']=result['id']
           answerDict['firstname']=result['toUser__first_name']
           answerDict['lastname']=result['toUser__last_name']
           answerDict['title']=result['title']
           answerDict['date']=result['date'].strftime("%m/%d/%Y, %H:%M:%S")
           resultList.append(answerDict)
           answerDict={}
       jsona=json.dumps(resultList)   
       return JsonResponse({"res":True, 'json':jsona})
    return JsonResponse({"res":False, 'message':"no messages"})



@token_req
@csrf_exempt
def getInbox_view(request, username):
    resultList=[]
    answerDict={}
    user=User.objects.get(username=username)
    getAllMessages=user.allMessages.all()
    results=getAllMessages.filter(deleteFromGetter=False).values('id', 'fromUser__first_name', 'fromUser__last_name', 'title', 'date').order_by('-date')
    if results:
       for result in results:
           answerDict['id']=result['id']
           answerDict['firstname']=result['fromUser__first_name']
           answerDict['lastname']=result['fromUser__last_name']
           answerDict['title']=result['title']
           answerDict['date']=result['date'].strftime("%m/%d/%Y, %H:%M:%S")
           resultList.append(answerDict)
           answerDict={}
       jsona=json.dumps(resultList)
       return JsonResponse({"res":True, 'json':jsona})
    return JsonResponse({"res":False, 'message':"inbox is empty"})


@token_req
@csrf_exempt
def sendMessage_view(request, fromUser, toUser):
    sender=User.objects.get(username=fromUser)
    getter=User.objects.get(username=toUser)
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    textOfMessage=body['messageText']
    titleOfMessage=body['messageTitle']
    if textOfMessage != "" :
       newMessage=message.objects.create(fromUser=sender, toUser=getter, title=titleOfMessage, messageText=textOfMessage)
       return JsonResponse({"res":True, "message": "message is sent successfully"})
    else:
       return JsonResponse({"res":False, "message": "message is empty , please add text"})




@token_req
@csrf_exempt
def singleMessage_view(request,  messageId):
    print("came here")
    _message={}
    theMessage=message.objects.get(id=messageId)
    if theMessage:
       print(theMessage)
       _message['text']=theMessage.messageText
       _message['textTitle']=theMessage.title
       _message['date']=theMessage.date.strftime("%m/%d/%Y, %H:%M:%S")
       _message['senderfname']=theMessage.fromUser.first_name
       _message['senderlname']=theMessage.fromUser.last_name
       user2=theMessage.toUser
       _message['getterfname']=theMessage.toUser.first_name
       _message['getterlname']=theMessage.toUser.last_name
       return JsonResponse({"res":True, "single": _message})
    else:
       return JsonResponse({"res":False, "message": 'message has not been found'})


@token_req
@csrf_exempt
def deleteMessage_view(request, username, messageId):
    theMessage=message.objects.get(id=messageId)
    if  theMessage.deleteFromGetter == True and str(theMessage.fromUser) == username:
        theMessage.delete()
        return JsonResponse({"res":True})
    if theMessage.deleteFromSender == True and str(theMessage.toUser)== username:
         theMessage.delete()
         return JsonResponse({"res":True})
    if str(theMessage.fromUser) == username:
       theMessage.deleteFromSender =True
       theMessage.save()
       return JsonResponse({"res":True})
    if str(theMessage.toUser) == username:
         theMessage.deleteFromGetter = True
         theMessage.save()
         return JsonResponse({"res":True})
    else:
         return JsonResponse({"res":False})

