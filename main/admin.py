from django.contrib import admin

# Register your models here.
from .models import Users, Record 
# admin.site.register(Users)
# admin.site.register(Record)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display: ('usr_id', 'user_name', 'pwd')
    # list_filter:('usr_id',)
    search_fields: ('usr_id',)

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display: ('usr_id', 'date', 'start_time', 'end_time', 'source', 'trigger_reason', 'timesCount')
    list_filter:('date', )