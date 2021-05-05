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
    results=allMessages.filter().values('id', 'toUser__first_name', 'toUser__last_name', 'title', 'date').order_by('-date')
    print(results)
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
    return JsonResponse({"res":True, 'message':"no messages"})



@token_req
@csrf_exempt
def getInbox_view(request, username):
    resultList=[]
    answerDict={}
    user=User.objects.get(username=username)
    getAllMessages=user.allMessages.all()
    results=allMessages.filter().values('id', 'fromUser__first_name', 'fromUser__last_name', 'title', 'date').order_by('-date')
    print(results)
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
    return JsonResponse({"res":True, 'message':"inbox is empty"})


@token_req
@csrf_exempt
def sendMessage_view(request, fromUser, toUser):
    sender=User.objects.get(username=fromUser)
    getter=User.objects.get(username=toUser)
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    textOfMessage=body['messageText']
    if textOfMessage != "" :
       newMessage=message.objects.create(fromUser=fromUser, toUSer=toUser, messageText=textOfMessage)
       return JsonResponse({"res":True, "message": "message is sent successfully"})
    else:
       return JsonResponse({"res":False, "message": "message is empty , please add text"})


@token_req
@csrf_exempt
def deleteMessage_view(request, username, messageId):
    theMessage=message.objects.get(id=messageId)
    if  theMessage.deleteFromGetter == True and theMessage.fromUser == username:
        theMessage.delete()
        return JsonResponse({"res":True})
    elif theMessage.deleteFromSender == True and theMessage.toUser == username:
         theMessage.delete()
         return JsonResponse({"res":True})
    elif theMessage.fromUser == username:
       theMessage.deleteFromSender =True
       theMessage.save()
       return JsonResponse({"res":True})
    elif theMessage.toUser == username:
         theMessage.deleteFromGetter = True
         theMessage.save()
         return JsonResponse({"res":True})
    else:
         return JsonResponse({"res":False})



@token_req
@csrf_exempt
def singleMessage_view(request,  messageId):
    message={}
    theMessage=message.objects.get(id=messageId)
    if theMessage:
       message['text']=theMessage.messageText
       message['textTitle']=theMessage.title
       message['date']=theMessage.date.strftime("%m/%d/%Y, %H:%M:%S")
       message['senderfname']=theMessage.fromUser__first_name
       message['enderlname']=theMessage.fromUser__last_name
       message['getterfname']=theMessage.toUser__first_name
       message['getterlname']=theMessage.toUser__last_name
       return JsonResponse({"res":True, "singleMessage": message})
    else:
       return JsonResponse({"res":False, "message": 'message has not been found'})