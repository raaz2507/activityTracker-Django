from django.contrib import admin

# Register your models here.
from .models import Users, Record 
admin.site.register(Users)
admin.site.register(Record)
