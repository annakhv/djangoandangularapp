from django.db import models
from django.contrib.auth.models import User

PERSONAL_STATUSES=[
    ('s', 'single'),
    ('m', 'married'),
    ('w', 'widowed'),
    ('r', 'in a relationship')
 
]

EDUCATION_TYPES=[
     ('High school', 'high school'),
     ('BA', 'bachelor of Arts'),
     ('Bsc', 'bachelor of Science'),
     ('MA', 'Master of arts'),
     ('Msc', 'Master of Science'),
     ('Phd', 'Doctorate'),
     
]


class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate=models.DateField(auto_now=False, auto_now_add=False,  null=True, blank=True)
    relationshipstatus=models.CharField(choices=PERSONAL_STATUSES, blank=True, null=True , max_length=50)
    origincountry=models.CharField(max_length=50, blank=True, null=True)
    currentcountry=models.CharField(max_length=50, blank=True, null=True)
    is_active=models.BooleanField(default=False, blank=True)
    following=models.ManyToManyField("self", blank=True,  symmetrical=False, related_name="follower")

   # def __repr__(self):
   #     return "%s born on %s from %s" (self.user, self.birthdate,  self.origincountry)



class education(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    educationType=models.CharField(choices=EDUCATION_TYPES, max_length=60)
    institution=models.CharField(max_length=100)
    startDate=models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    endDate=models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    country=models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return  "%s studied %s at %s" (self.user, self.educationType, self.institution)

class workPlace(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    company=models.CharField(max_length=100)
    startDate=models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    endDate=models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    country=models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return "%s worked %s at %s" (self.user, self.place, self.company)