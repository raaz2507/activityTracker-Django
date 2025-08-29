from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = "home" ),
    path('about/', views.about_page_view, name='about'),

    # login and singup 
    path( 'login/', views.login_view, name = "login" ),
    path('logout/', views.logout_view, name='logout'),
    path( 'signup/', views.singup_view, name="signup" ),
     path('change_user_profile/<int:user_id>/', views.change_user_profile, name='change_user_profile'),

    # #record related 
    path('selectActivity/', views.selectActivity_view, name='selectActivity'),
    path('addRecord/<int:pk>/', views.add_record_view, name='addRecord'),
    path('viewRecord/', views.viewRecordPage, name=  'viewRecord'),
    path('updateRecord/<int:record_id>', views.record_edit_view, name= 'record_edit'),
    path('record/delete/<int:record_id>/', views.record_delete_view, name='record_delete'),
    
    #record reprentations
    # calander urls
    # path('calander/', views.calander_view, name='calander'),
    path('calendar/', views.yearly_calendar, name='yearly_calendar'),
    path('calendar/<int:year>/', views.yearly_calendar, name='yearly_calendar_by_year'),

    #charts view
    path('charts/', views.chart_view, name="charts"),

    # #mange Accounts
    path('usr_acc_man/',  views.userAccountManage, name='userAccountManage'),
    path('usr_acc_man/<int:user_id>/',  views.userAccountManage, name='getUserData'),
    # path('usr_acc_man/delete/<slug:del_user_id>/',  views.userAccountManage, name='delUserData'),


]