from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse



@csrf_exempt
def register_view(request):
    print("hello world")
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    username=body['username']
    fname=body['firstname']
    lname=body['lastname']
    email=body['email']
    password=body['password']
    _password=body['repeatpassword']
    num = 0
    lenList= [len(username), len(fname) , len(lname) , len(email) , len(password)]
    digitInPassword=[p for p in password if p in "1234567890"]
    if  num  in lenList:
        message="please fill in  all the  fields"
    elif User.objects.filter(username=username).count() > 0:
        message="this username is already in use"
    elif password != _password:
        message="passwords do not match"
    elif len(password) < 6:
        message= "password  should contain at least 6 characters"
    elif len(digitInPassword) == 0:
    
        message= "password should contain at least one digit"
    else:
        message="ok"
        user=User.objects.create_user(username,  email, password)
        user.first_name=fname
        user.last_name=lname
        user.save()

    data={
        "message" : message
    }
    return JsonResponse(data)
  

@csrf_exempt
def login_view(request):
    body_unicode=request.body.decode('utf-8')
    body=json.loads(body_unicode)
    username=body['username']
    password=body['password']
    user=authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"res" : True})
    return JsonResponse({"res" : False})




def logout_view(request):
    return True
