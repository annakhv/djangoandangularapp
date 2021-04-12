from django.contrib import admin
#from django.contrib.auth.models import User
from .models import  profile, education, workPlace



#admin.site.register(User),
admin.site.register(profile),
admin.site.register(education),
admin.site.register(workPlace),