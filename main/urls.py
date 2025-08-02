from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = "home" ),

    # login and singup 
    path( 'login/', views.login, name = "login" ),
    path( 'signup/', views.singup, name="signup" ),
    path('logout/', views.logout, name='logout'),

    #record related 
    path('addRecord/', views.RecordFormPage, name='addRecord'),
    path('viewRecord/', views.viewRecordPage, name=  'viewRecord'),
    path('viewRecord/<int:id>/', views.RecordFormPage, name= 'record_edit'),
    path('viewRecord/delete/<int:id>/', views.record_delete, name='record_delete'),
    
    #record reprentations
    # calander urls
    # path('calander/', views.calander_view, name='calander'),
    path('calendar/', views.yearly_calendar, name='yearly_calendar'),
    path('calendar/<int:year>/', views.yearly_calendar, name='yearly_calendar_by_year'),

    #charts view
    path('charts/', views.chart_view, name="charts"),

]