from django.contrib import admin

#from django.contrib.auth.models import User
from .models import question, answer, comment



#admin.site.register(User),
admin.site.register(question),
admin.site.register(answer),
admin.site.register(comment),
