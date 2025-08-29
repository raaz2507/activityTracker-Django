from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator, MaxValueValidator

class myuser(AbstractUser):
    phone= models.CharField(max_length=10, unique=True)
    gender= models.CharField(max_length=10, choices=[('male', 'Male'),('female', 'Female'), ('other', 'Other')], default='male')
    age = models.IntegerField(validators=(MinValueValidator(0),MaxValueValidator(100)), default=1, null=False)
    def __str__(self):
        return f"id:{self.id } usr_name:"+super().__str__()

from colorfield.fields import ColorField
class activity_schema(models.Model):
    activity_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    slug = models.CharField(max_length=50, unique=True, null=False, blank= False)
    color_field = ColorField(default='#FFFFFF')
    source = models.JSONField(null=False, blank=False)
    trigger = models.JSONField(null=False, blank=False)
    extra = models.JSONField(null=False, blank=False, default=dict)

    def __str__(self):
        return f"{self.id}-{self.activity_name}- {self.source} - {self.trigger} - {self.extra}"
    
class usersDefine_activity_schema(models.Model):
    usr_id = models.ForeignKey(
        myuser,
        on_delete= models.CASCADE,
        related_name= 'usersDefine_activity_schema'
    )
    activity_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    slug = models.CharField(max_length=50, unique=True, null=False, blank= False)
    source = models.JSONField(null=False, blank=False)
    trigger = models.JSONField(null=False, blank=False)
    extra = models.JSONField(null=False, blank=False, default=dict)
    favtrate = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return f"{self.usr_id}- {self.activity_name}- {self.source}- {self.trigger}- {self.extra} - {self.favtrate}"


class userRecords(models.Model):
    usr_id = models.ForeignKey(
        myuser,
        on_delete= models.CASCADE, # अगर user delete होगा तो उसकी सारी records भी delete होंगी
        related_name='activity_record'  # user.records से access कर सकते हैं
    )
    date = models.DateField()
    start_time =  models.TimeField(null=False, blank=False , )
    end_time =  models.TimeField(null=False, blank=False )
    activity_name = models.CharField(max_length=50, null=False, blank=False)
    source = models.JSONField(null=False, blank=False)
    trigger = models.JSONField(null=False, blank=False)
    extra = models.JSONField(null=False, blank=False, default=dict)

    def __str__(self):
        return f"{self.usr_id}{self.date}- {self.start_time}- {self.end_time} {self.activity_name}"

