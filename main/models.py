from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class myuser(AbstractUser):
    phone= models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}$')])
    gender= models.CharField(max_length=10, choices=[('male', 'Male'),('female', 'Female'), ('other', 'Other')], default='male')
    age = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], default=1, null=False)
    def __str__(self):
        return f"id:{self.id } usr_name:"+super().__str__()

from colorfield.fields import ColorField
from django.utils.text import slugify

class activity_schema(models.Model):
    usr_id = models.ForeignKey(
        myuser,
        on_delete= models.CASCADE,
        related_name= 'activity_schema',
        null= True,
        blank= True,
    )
    activity_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    icon =  models.FileField(upload_to= 'Activity_icons/', null=True, blank=True, default='Activity_icons/default_icon.svg')
    # height = models.IntegerField(null=True, blank=True)
    # width = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, null=False, blank= False)
    color_field = ColorField(default='#FFFFFF')
    source = models.JSONField(null=False, blank=False, default=dict)
    trigger = models.JSONField(null=False, blank=False, default=dict)
    extra = models.JSONField(null=False, blank=False, default=dict)

   
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.activity_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.activity_name}- {self.slug}"
    
from django.conf import settings
class userFavrateActivity(models.Model):
    usr_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'favorite_activities',
        unique=False
    )
    activity_id =  models.ForeignKey(
        activity_schema,
        on_delete= models.CASCADE,
        related_name= 'favored_by_users',
        unique=False
    )
    class Meta:
        unique_together = ('usr_id', 'activity_id');

    def __str__(self):
        return f"{self.usr_id}- {self.activity_id}"


class userRecords(models.Model):
    usr_id = models.ForeignKey(
        myuser,
        on_delete= models.CASCADE, # अगर user delete होगा तो उसकी सारी records भी delete होंगी
        related_name='activity_record'  # user.records से access कर सकते हैं
    )
    date = models.DateField()
    start_time =  models.TimeField(null=False, blank=False , )
    end_time =  models.TimeField(null=False, blank=False )
    activity_id = models.ForeignKey(
        activity_schema,
        on_delete= models.CASCADE,
        related_name= 'activities_obj',
        unique=False,
        null=False,
        blank=False,
    )
    source = models.JSONField(null=False, blank=False)
    trigger = models.JSONField(null=False, blank=False)
    extra = models.JSONField(null=False, blank=False, default=dict)

    def __str__(self):
        return f"{self.usr_id}{self.date}- {self.start_time}- {self.end_time} {self.activity_id.activity_name}"

