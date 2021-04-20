from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class  question(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    date=models.DateField(auto_now_add=True)
    question=models.CharField(max_length=1000)


class answer(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    whichQuestion=models.ForeignKey(question,  on_delete=models.CASCADE)
    answer=models.TextField()
    date=models.DateField(auto_now_add=True)
    upVotes=models.PositiveIntegerField()


class comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    whichAnswer=models.ForeignKey(question,  on_delete=models.CASCADE)
    comment=models.TextField()
    date=models.DateField(auto_now=True)