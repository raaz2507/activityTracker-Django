from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import myuser, userRecords, activity_schema, userFavrateActivity


@admin.register(myuser)
class myuserAdmin(UserAdmin):
    model =  myuser
    fieldsets = UserAdmin.fieldsets + (('Extra Info', {'fields': ('phone', 'gender', 'age')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('phone', 'gender', 'age')}),
    )

    list_display = ['username', 'email', 'phone', 'gender', 'age']

    list_filter = ['gender', 'age']

@admin.register(userRecords)
class userRecordsAdmin(admin.ModelAdmin):
    list_display = ['usr_id', 'date', 'start_time', 'end_time', 'activity_id'] 
    list_filter = ['date', 'usr_id']  # optional: filter sidebar
    search_fields = ['usr_id']  # optional: search box


@admin.register(activity_schema)
class activity_schemaAdmin(admin.ModelAdmin):
    list_display = ['id','activity_name','icon', 'color_field', 'trigger','source', 'extra']
    list_filter = ['activity_name']
    search_fields = ['activity_name']

@admin.register(userFavrateActivity)
class userFavrateActivity_Admin(admin.ModelAdmin):
    list_display = ['usr_id', 'activity_id']
    list_filter = ['usr_id', 'activity_id']
    search_fields = ['usr_id', 'activity_id']