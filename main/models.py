from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.
# from django.contrib.auth import get_user_model
# users= get_user_model()
class Users(models.Model):
    def save(self, *args, **kwargs):
        if not self.usr_id:
            last_user = Users.objects.order_by('-id',).first()
            if last_user and last_user.usr_id:
                lastNumber = int(last_user.usr_id.split('_')[1])
                self.usr_id =  f"usr_{lastNumber + 1:02d}"
            else:
                self.usr_id =  "usr_01"
        super().save(*args, **kwargs)


    usr_id =  models.CharField(max_length=10, unique = True, null=False, editable= False)
    user_name = models.CharField( max_length=10 , unique=True, null=False)
    pwd = models.CharField( max_length=4 , null=False)

    def __str__(self):
        return f"ID: {self.usr_id}, U: {self.user_name}, P: {self.pwd}"



class Record(models.Model):
    class SourceChoice(models.TextChoices):
        videos = 'videos', 'videos'
        books = 'books', 'books'
        comics =  'comics', 'comics'
        interction = 'interction', 'interction'
        chat = 'chat', 'chat'

    class TriggerReasonFilde(models.TextChoices):
        digitalVisual = 'Digital visual', 'Digital visual'
        social_interaction = 'social interaction', 'social interaction'
        hadNotDoFromLastLong = 'hadNotDoFromLastLong', 'hadNotDoFromLastLong'



    usr_id =  models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField( null=False)
    start_time = models.TimeField( null=False)
    end_time =  models.TimeField( blank=True, null=True)
    # source = models.CharField(choices=SourceChoice.choices , max_length=65, default=SourceChoice.videos)
    source = MultiSelectField(choices=SourceChoice.choices , max_length=65, default=SourceChoice.videos)
    # trigger_reason =models.CharField(choices=TriggerReasonFilde.choices, max_length=65, default=TriggerReasonFilde.digitalVisual)
    trigger_reason =MultiSelectField(choices=TriggerReasonFilde.choices, max_length=65, default=TriggerReasonFilde.digitalVisual)
    timesCount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.date}, {self.start_time}, {self.end_time}, {self.source}"