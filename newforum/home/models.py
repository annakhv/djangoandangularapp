from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class  question(models.Model):
    user=models.ForeignKey(User)
    date=models.DateField(auto_now=True)
    question.models.CharField(max_length=None)


class answer(models.Model):
    user=models.ForeignKey(User)
    whichQuestion=models.ForeignKey(question,  on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    upVotes=models.PositiveIntegerField()


class comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    whichAnswer=models.ForeignKey(question,  on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)