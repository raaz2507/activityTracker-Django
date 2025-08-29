from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import myuser, userRecords


@admin.register(myuser)
class myuserAdmin(UserAdmin):
    model =  myuser
    fieldsets = UserAdmin.fieldsets + (('Extra Info', {'fields': ('phone', 'gender')}),)
    # (('Extra Info', {'fields': ('phone', 'gender')}))
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('phone', 'gender')}),
    )

    list_display = ['username', 'email', 'phone', 'gender']

    list_filter = ['gender']

@admin.register(userRecords)
class userRecordsAdmin(admin.ModelAdmin):
    list_display = ['usr_id', 'date', 'start_time', 'end_time', 'activity_name'] 
    list_filter = ['date', 'usr_id']  # optional: filter sidebar
    search_fields = ['usr_id']  # optional: search box

from .models import activity_schema, usersDefine_activity_schema

@admin.register(activity_schema)
class activity_schemaAdmin(admin.ModelAdmin):
    list_display = ['id','activity_name', 'color_field', 'source', 'trigger', 'extra']
    list_filter = ['activity_name']
    search_fields = ['activity_name']

@admin.register(usersDefine_activity_schema)
class usersDefine_activity_schemaAdmin(admin.ModelAdmin):
    list_display = ['usr_id', 'activity_name', 'source', 'trigger', 'extra', 'favtrate']
    list_filter = ['usr_id', 'activity_name', 'favtrate']
    search_fields = ['usr_id', 'activity_name']