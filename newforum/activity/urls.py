from django.contrib import admin
from django.urls import path
from activity import views

urlpatterns=[
  path('personalActivity/<username>', views.personalActivity_view, name="personalActivity"),
  path('activeUsers/<username>', views.activeUsers_view, name="activeUsers"),
  path('getSentMessages/<username>', views.getSentMessages_view, name="getSentMessages"),
  path('getInbox/<username>', views.getInbox_view, name="getInbox"),
  path('sendMessage/<fromUser>/<toUser>', views.sendMessage_view, name='sendMessage'),
  path('deleteMessage/<username>/<messageId>', views.deleteMessage_view, name='deleteMessage'),
  path('singleMessage/<messageId>', views.deleteMessage_view, name="singleMessage")
]