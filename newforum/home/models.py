from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class  question(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    date=models.DateField(auto_now_add=True)
    userQuestion=models.CharField(max_length=1000)

  #  def __str__(self):
   #     return self.userQuestion

class answer(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    whichQuestion=models.ForeignKey(question,  on_delete=models.CASCADE)
    userAnswer=models.TextField()
    date=models.DateField(auto_now_add=True)
    upVotes=models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.userAnswer


class comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    whichAnswer=models.ForeignKey(question,  on_delete=models.CASCADE)
    userComment=models.TextField()
    date=models.DateField(auto_now=True)
    def __str__(self):
        return self.userComment