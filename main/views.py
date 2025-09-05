from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import loginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    usr = request.session.get('login_user')
    return render(request, 'home.html')
def about_page_view(request):
    user = request.session.get('login_user')
    
    return render(request, 'about.html')

def login_view(request):
    if request.method == "POST":
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd =  form.cleaned_data.get('password')
            user =  authenticate(request , username= uname, password= pwd)
            if user is not None:
                login(request, user)
                next_url =  request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home')
            else:
                messages.error(request, "Username not exists or password does not match")

    else:
        form =  loginForm()
    # GET request ke liye bhi 'next' pass karna hoga
    next_url = request.GET.get('get', '')
    
    return render(request, "login.html",{'form':form, 'next': next_url}) 


def logout_view( request ):
    request.session.flush()  # पूरे session को clear कर देगा
    logout(request)  # session और user authentication clear हो जाएगी
    return redirect('login')  # redirect to login page या किसी और page पर


def singup_view(request):
    if request.method == "POST":
        form=  SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # signup होते ही login करा देंगे
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "singup.html", {'form': form})

from .models import myuser
from django.shortcuts import get_object_or_404
from .forms import UserUpdateForm

@login_required(login_url= 'home')
def change_user_profile(request, user_id):
    user = get_object_or_404(myuser, id = user_id)
    if request.method == "POST":
        form= UserUpdateForm(request.POST, instance= user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance = user)
    
    return render(request, 'singup.html', {"form": form})

# record related functions

from .models import activity_schema, userFavrateActivity

@login_required( login_url = 'login')
def selectActivity_view(request):
    pre_activites =  activity_schema.objects.filter(usr_id=None)
    favrateActivitysList =  list(userFavrateActivity.objects.filter(usr_id= request.user).values_list('activity_id', flat=True))
    userDefineActiviyAll =  activity_schema.objects.filter(usr_id= request.user)
    
    activites=[]
    favrateActivitys =[]
    for act in pre_activites:
        if act.id in favrateActivitysList:
            favrateActivitys.append(act)
        else:
            activites.append(act)

    userDefineActiviy =[]
    for act in userDefineActiviyAll:
        if act.id in favrateActivitysList:
            favrateActivitys.append(act)
        else:
            userDefineActiviy.append(act)
    print(userDefineActiviy)
    # print(favrateActivitys)
    # print(activites)
    return render(request, 'selectActivity.html', {'all_activities':activites, 'userDefineActiviy': userDefineActiviy, 'favrateActivitys':favrateActivitys})

# activites_slugify_map={ slugify(activite.activity_name): activite.activity_name for activite in activity_schema.objects.all()}


def toggleFavActivity(request, activity_id):
    if request.user.is_authenticated:
        try:
            activity = get_object_or_404(activity_schema, id=activity_id)

            # Check if already exists
            fav_entry = userFavrateActivity.objects.filter(
                usr_id=request.user,
                activity_id=activity
            ).first()

            if fav_entry:
                # अगर मौजूद है तो delete कर दो
                fav_entry.delete()
                return JsonResponse({
                    "success": True,
                    "action": "removed",
                    "message": "Activity removed from favorites"
                })
            else:
                # नहीं है तो add करो
                userFavrateActivity.objects.create(
                    usr_id=request.user,
                    activity_id=activity
                )
                return JsonResponse({
                    "success": True,
                    "action": "added",
                    "message": "Activity added to favorites"
                })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })
    else:
        return JsonResponse({
            "success": False,
            "message": "User not authenticated"
        })


from .forms import ActivitySchemaForm
@login_required(login_url='login')
def add_new_activty_view(request):
    if request.method == "POST":
        form = ActivitySchemaForm(request.POST, request.FILES)
        if form.is_valid():
            new_activity = form.save(commit=False)
            new_activity.usr_id =  request.user
            new_activity.save()
            messages.success(request, "new Acctiviy addess sussesfuly")
            print("susssse")
            return redirect('selectActivity')
        else:
            print("error")
            messages.error(request, "get error to save new activity.")
            # form = ActivitySchemaForm()  
    else:
        print("new form")
        form = ActivitySchemaForm()
    return render(request, "addNewActivity.html",{ "form": form })
@login_required(login_url='login')
def edit_new_activty_view(request, activityId):
    activity =  get_object_or_404(activity_schema, usr_id = request.user, pk = activityId)
    if request.method == "POST":
        form = ActivitySchemaForm(request.POST, request.FILES, instance= activity)
        if form.is_valid:
            form.save()
            messages.success(request, "Activiy Update sussesfuly")
            return redirect('selectActivity')
        else:
            messages.error(request, "cant Update activity.")
            form = ActivitySchemaForm(instance= activity)

    else:
        form = ActivitySchemaForm(instance= activity)
    return render(request, "addNewActivity.html",{ "form": form }) 
@login_required(login_url='login')
def del_new_activty_view(request, activityId):
    obj = get_object_or_404( activity_schema, usr_id = request.user ,pk =  activityId)
    obj.delete()
    return redirect('selectActivity')


from .forms import userRecordsForm

@login_required(login_url= 'login')
def add_record_view(request, pk):
    activity = get_object_or_404(activity_schema, pk=pk)

    if request.method == "POST":
        form = userRecordsForm(activity, request.POST)
        form.schema = activity  # form को schema instance attach
        if form.is_valid():
            record = form.save(commit=False)
            record.usr_id = request.user
            record.activity_id = activity
            record.save()
            messages.success(request, "Record saved successfully!")
            return redirect('viewRecord')
    else:
        form = userRecordsForm(activity)
        form.schema = activity

    return render(request, "record_form.html", {"form": form, "activity": activity, "messages": messages })



from .models import userRecords

@login_required(login_url= 'login')
def record_edit_view(request, record_id):
    record = get_object_or_404(userRecords, pk=record_id)
    activity = get_object_or_404(activity_schema, pk=record.activity_id.id)

    if request.method == "POST":
        form = userRecordsForm(activity, request.POST, instance=record)
        form.schema = activity
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Record updated successfully!")
            return redirect("viewRecord")
        else:
            messages.error(request, "⚠️ Please fix the errors.")
    else:
        # JSON True/False dict को form checkboxes में convert करना
        initial_data = {
            'date': record.date,
            'start_time': record.start_time,
            'end_time': record.end_time,
            'source': [k for k,v in record.source.items() if v],
            'trigger': [k for k,v in record.trigger.items() if v],
            'extra': [k for k,v in record.extra.items() if v],
        }
        form = userRecordsForm(activity, initial=initial_data)
        form.schema = activity

    return render(request, 'record_form.html', {"form": form, "activity": activity, "messages": messages})



@login_required(login_url= 'login')
def viewRecordPage(request):
    records = userRecords.objects.filter(usr_id = request.user)
    return render(request, 'viewRecord.html', {'data': records })

@login_required(login_url='login')
def record_delete_view(request, record_id):
    record = get_object_or_404(userRecords, pk=record_id)

    if request.method == "POST":
        record.delete()
        messages.success(request, "✅ Record deleted successfully!")
        return redirect("viewRecord")  # Redirect back to record list
    else:
        messages.error(request, "⚠️ Invalid request method.")
        return redirect("viewRecord")


''' chart releted function end '''

# #chart views
import json
from django.db.models import Count
@login_required(login_url='login')
def chart_view(request):
    activity_meta = getuserActiviyList(request)
    print(activity_meta)
    return render(request, 'charts.html', {'activity_meta': activity_meta})


from django.conf import settings
def getuserActiviyList(request):
     # Step 1: सब activity_ids लें
    activity_ids = userRecords.objects.filter(usr_id=request.user).values_list("activity_id", flat=True).distinct()
    
    charts_meta={}
    for act_id in activity_ids:
        schema = activity_schema.objects.filter(id = act_id).values('id', 'color_field','activity_name','icon').first()
        if schema:
            charts_meta[act_id] ={
                'id' : schema['id'],
                'color': schema['color_field'] or '#fff',
                'activity_name': schema['activity_name'],
                'icon_url': request.build_absolute_uri(settings.MEDIA_URL + schema['icon']) if schema['icon'] else None,
            }
    return charts_meta

# 🔹 Common helper for filtering by period
def filter_by_period(qs, year, month, day):
    if year and month and day:
        # Exact day filter
        qs = qs.filter(date__year=year, date__month=month, date__day=day)
    elif year and month:
        # Whole month filter
        qs = qs.filter(date__year=year, date__month=month)
    elif year:
        # Whole year filter
        qs = qs.filter(date__year=year)
    # else:
        # today = date.today()
        # Default = today
        # qs = qs.filter()

    return qs

def get_activity_summary(request, act_id, field, year, month, day):
    """
    Common helper function for source/trigger chart data
    field: "source" या "trigger"
    """
    schema = activity_schema.objects.filter(id=act_id).values('color_field', 'activity_name', field).first()
    activity_summary = {}

    if schema:
        activity_summary = {
            'activity_name': schema['activity_name'],
            field: {k: 0 for k in (schema[field] or {}).keys()},
        }

    today = date.today()
    qs = userRecords.objects.filter(
        usr_id=request.user,
        activity_id=act_id
    ).values('date', field)

    # Period filter
    qs = filter_by_period(qs, year, month, day)

    records = qs.values('start_time', 'end_time', field)

    # Counting logic
    for rec in records:
        for key, value in rec[field].items():
            if value:
                activity_summary[field][key] += 1

    return activity_summary


# -------- Views -----------
def TriggerChartData_view(request, act_id, year=None, month=None, day=None):
    data = get_activity_summary(request, act_id, "trigger", year, month, day)
    return JsonResponse(data)


def SourceChartData_view(request, act_id, year=None, month=None, day=None):
    data = get_activity_summary(request, act_id, "source", year, month, day)
    return JsonResponse(data)

from  datetime import datetime, date, time
def TimeDurationData_view(request, act_id, year=None, month=None, day=None):
    today = date.today()
    qs = userRecords.objects.filter(usr_id=request.user,activity_id=act_id).values('date', 'start_time', 'end_time')

    qs = filter_by_period(qs, year, month, day)
    # "all" में कोई filter नहीं
    records =qs.values('start_time', 'end_time' )
    
    # Duration calculate करना (minutes में)
    total_duration_minutes = 0
    for rec in records:
        start_time = rec['start_time']
        end_time = rec['end_time']

        
        if start_time and end_time:
            # Django timeField return करता है time object
            duration = datetime.combine(today, end_time) - datetime.combine(today, start_time)
            duration_minutes = duration.total_seconds() / 60
            total_duration_minutes += duration_minutes
        
    return JsonResponse({'total_duration_minutes': total_duration_minutes})

# def chartData_view_old(request, period="all"):
#     # Step 1: सब activity_ids लें
#     activity_ids = userRecords.objects.filter(usr_id=request.user).values_list("activity_id", flat=True).distinct()
    
#     activity_summary = {}
#     for act_id in activity_ids:
#         schema = activity_schema.objects.filter(id = act_id).values('color_field','activity_name','icon','source', 'trigger').first()
#         if schema:
#             source = schema['source'].keys() if schema['source'] else []
#             trigger = schema['trigger'].keys() if schema['trigger'] else []
#             activity_summary[act_id]={
#                 'color': schema['color_field'] or '#fff',
#                 'activity_name': schema['activity_name'],
#                 'icon_url': request.build_absolute_uri(settings.MEDIA_URL + schema['icon']) if schema['icon'] else None,
#                 'source' : {k: 0 for k in (schema['source'] or {}).keys()}, # हर source key की initial value 0
#                 'trigger': {k: 0 for k in (schema['trigger'] or {}).keys()}, # हर trigger key की initial value 0
#                 'total_duration_minutes': 0  # duration जोड़ने के लिए
#             }

#     # print(activity_summary.keys())
#     # Step 2: queryset में time filter लगाएँ
#     today = date.today()
#     records={}
#     for act_id in activity_ids:
#         qs = userRecords.objects.filter(usr_id=request.user,activity_id=act_id).values('date', 'start_time', 'end_time', 'source', 'trigger')
        
#         period = period.lower()
#         if period == "today":
#             qs = qs.filter(date=today)
#         elif period == "month":
#             qs = qs.filter(date__year=today.year, date__month=today.month)
#         elif period == "year":
#             qs = qs.filter(date__year=today.year)
#         # "all" में कोई filter नहीं
#         records[act_id] =qs.values('start_time', 'end_time', 'source', 'trigger')
    
#     # Step 3: source/trigger counting
#     for act_id in records:
#         for rec in records[act_id]:
#             for key, value in rec['source'].items():
#                 if value:
#                     # if isinstance(activity_summary[act_id]['source'][key], str):
#                     #     activity_summary[act_id]['source'][key] = 0
#                     activity_summary[act_id]['source'][key] +=1
            
#             for key, value in rec['trigger'].items():
#                 if value:
#                     # if isinstance(activity_summary[act_id]['trigger'][key], str):
#                     #     activity_summary[act_id]['trigger'][key] = 0
#                     activity_summary[act_id]['trigger'][key] +=1

#             # Duration calculate करना (minutes में)
#             start_time = rec['start_time']
#             end_time = rec['end_time']
#             if start_time and end_time:
#                 # Django timeField return करता है time object
#                 duration = datetime.combine(today, end_time) - datetime.combine(today, start_time)
#                 duration_minutes = duration.total_seconds() / 60
#                 activity_summary[act_id]['total_duration_minutes'] += duration_minutes

#     # print(activity_summary[2].keys())    
#     # print(activity_summary)
#     return JsonResponse( {'chart_data' : activity_summary})


@login_required(login_url='login')
def calendar_view(request):
    return render(request, 'calendar.html')
    
from django.db.models import F
@login_required(login_url='login')
def get_calandar_data(request, year):
    user_records={}
    if isinstance(year, int):
        user_records = userRecords.objects.filter(
                usr_id= request.user, 
                date__year= year
            ).annotate(
                activity_name =F("activity_id__activity_name"),
                color=F("activity_id__color_field"),
            ).values(
                'activity_name', 'color', 'date', 'start_time', 'end_time', 'source', 'trigger', 'extra',
            )
        print(list(user_records))
        return JsonResponse(list(user_records), safe=False)
    
    return JsonResponse({'error': "invalid year"}, status= 400)



# from datetime import datetime
# import calendar ,json

# from bs4 import BeautifulSoup  # पहले ensure करें कि यह install है: pip install beautifulsoup4 
# @login_required(login_url='login')
# def yearly_calendar(request, year=None):
#     if year is None:
#         year = datetime.now().year

#     usr = request.session.get('user')
#     user_records = userRecords.objects.filter(usr_id = request.user)
#     record_dates = [rec.date for rec in user_records if rec.date.year == year]

#     cal = calendar.HTMLCalendar(calendar.SUNDAY)
#     months = []
#     months_json_data = []

#     for month in range(1, 13):
#         month_name = calendar.month_name[month]
#         html_month = cal.formatmonth(year, month)

#         month_record_days = [d.day for d in record_dates if d.month == month]

#         # ✅ अब HTML में marked days को class दो
#         soup = BeautifulSoup(html_month, 'html.parser')
#         for td in soup.find_all('td'):
#             try:
#                 day = int(td.get_text(strip=True))
#                 if day in month_record_days:
#                     td['class'] = td.get('class', []) + ['marked-day']
#             except ValueError:
#                 pass  # Empty or non-numeric tds

#         final_html_month = str(soup)

#         months.append({
#             'name': month_name,
#             'html': final_html_month,
#             'marked_days': month_record_days,
#             'month_number': month,
#         })

#         months_json_data.append({
#             'name': month_name,
#             'marked_days': month_record_days,
#             'month_number': month,
#         })

#     months_json_data = json.dumps(months_json_data)

#     return render(request, 'calendar.html', {
#         'year': year,
#         'months': months,
#         'months_json': months_json_data, 
#         'user': request.user,
#     })


from django.http import JsonResponse
def userAccountManage(request, user_id=None, del_user_id=None):
    # print(user_id, del_user_id)
    if del_user_id:
        user = get_object_or_404(myuser, usr_id = del_user_id)
        # user.delete()
        userAccData = list(myuser.objects.all().values('id','user_name', 'gender', 'age', 'pwd' ))
        return JsonResponse({'userAccData':userAccData, 'messages':{'tag':"sussess", 'msg':f"{del_user_id} data Sussefuy Deleted..."}}, safe=False)
    if user_id:
        userData = list(userRecords.objects.filter(usr_id=user_id).values('id', 'usr_id__username', 'activity_name', 'date', 'start_time', 'end_time', 'source', 'trigger'))
        # userData = list(userRecords.objects.filter(usr_id__id=user_id).values( 'usr_id','date', 'start_time', 'end_time', 'activity_name', 'trigger', 'source', 'extra'))
        # print(userData)
        return JsonResponse(userData, safe=False);
    else:
        all_users = myuser.objects.all()
        print(all_users)
        return render(request, 'userAccountManage.html', {'all_users': all_users})

# def userAccountManageDeleteUsr(request, user_id):
#     user = get_object_or_404(Users, usr_id=user_id);
#     user.delete();
