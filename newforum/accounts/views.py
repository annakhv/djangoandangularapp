from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.

@csrf_exempt
def register_view(request):
    print("hello world")
    print(request.body)
 
    data={
        "here":True 
    }
    return JsonResponse(data)
  

@csrf_exempt
def login_view(request):
    print("hiii")
    return true
