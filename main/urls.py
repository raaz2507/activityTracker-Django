from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = "home" ),
    path('about/', views.about_page_view, name='about'),

    # login and singup 
    path( 'login/', views.login_view, name = "login" ),
    path( 'logout/', views.logout_view, name='logout'),
    path( 'signup/', views.singup_view, name="signup" ),
    path('profile_settings/', views.ProfileSettingsView, name="profile_settings" ),
    path( 'change_user_profile/<int:user_id>/', views.change_user_profile, name='change_user_profile'),
    path('bd/' ,views.backupAccoutData_view, name = "backupData"),
    path('rd/' ,views.restoreAccountData_view, name = "restoreData"),

    # Activity related 
    path('selectActivity/', views.selectActivity_view, name='selectActivity'),
    path('toggleFavActivity/<int:activity_id>/', views.toggleFavActivity, name='toggleFavActivity'),
    path('add_new_activty/', views.add_new_activty_view, name= "add_new_activty"),
    path('del_new_activty/<int:activityId>/', views.del_new_activty_view, name= "del_new_activty"),
    path('dedit_new_activty/<int:activityId>/', views.edit_new_activty_view, name= "edit_new_activty"),
    
    #record relatd crud
    path('addRecord/<int:pk>/', views.add_record_view, name='addRecord'),
    path('viewRecord/', views.viewRecordPage, name=  'viewRecord'),
    path('updateRecord/<int:record_id>', views.record_edit_view, name= 'record_edit'),
    path('record/delete/<int:record_id>/', views.record_delete_view, name='record_delete'),
    
    #record reprentations
    # calander urls
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar_data/<int:year>/', views.get_calandar_data, name='get_calandar_data'),
    # path('calendar/<int:year>/', views.yearly_calendar, name='yearly_calendar_by_year'),

    #charts view
    path('charts/', views.chart_view, name="charts"),
    
    path('TriggerChartData/<int:act_id>/', views.TriggerChartData_view, name="TriggerChartData"),
    path('TriggerChartData/<int:act_id>/<int:year>/', views.TriggerChartData_view, name="TriggerChartData"),
    path('TriggerChartData/<int:act_id>/<int:year>/<int:month>/', views.TriggerChartData_view, name="TriggerChartData"),
    path('TriggerChartData/<int:act_id>/<int:year>/<int:month>/<int:day>/', views.TriggerChartData_view, name="TriggerChartData"),
    
    path('SourceChartData/<int:act_id>/', views.SourceChartData_view, name="SourceChartData_view"),
    path('SourceChartData/<int:act_id>/<int:year>/', views.SourceChartData_view, name="SourceChartData_view"),
    path('SourceChartData/<int:act_id>/<int:year>/<int:month>/', views.SourceChartData_view, name="SourceChartData_view"),
    path('SourceChartData/<int:act_id>/<int:year>/<int:month>/<int:day>/', views.SourceChartData_view, name="SourceChartData_view"),
    
    path('time_duration_chart/<int:act_id>/', views.TimeDurationData_view, name="time_duration_chart"),
    path('time_duration_chart/<int:act_id>/<int:year>/', views.TimeDurationData_view, name="time_duration_chart"),
    path('time_duration_chart/<int:act_id>/<int:year>/<int:month>/', views.TimeDurationData_view, name="time_duration_chart"),
    path('time_duration_chart/<int:act_id>/<int:year>/<int:month>/<int:day>/', views.TimeDurationData_view, name="time_duration_chart"),
    


    # #mange Accounts
    path('usr_acc_man/',  views.userAccountManage, name='userAccountManage'),
    path('usr_acc_man/<int:user_id>/',  views.userAccountManage, name='getUserData'),
    # path('usr_acc_man/delete/<slug:del_user_id>/',  views.userAccountManage, name='delUserData'),


]