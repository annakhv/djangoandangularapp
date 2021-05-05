from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class message(models.Model):
    fromUser=models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    toUser=models.ForeignKey(User, on_delete=models.CASCADE, related_name="allMessages")
    messageText=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    deleteFromSender=models.BooleanField(default=False)
    deleteFromGetter=models.BooleanField(default=False)
    
    def __str__(self):
        return self.messageText