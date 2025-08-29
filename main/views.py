from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import loginForm, singupForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    usr = request.session.get('login_user')
    return render(request, 'home.html', { 'userName':usr})
def about_page_view(request):
    user = request.session.get('login_user')
    
    return render(request, 'about.html', { 'user': request.user})

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
    
    return render(request, "login.html",{ 'user':request.user, 'form':form, 'next': next_url}) 


def logout_view( request ):
    request.session.flush()  # पूरे session को clear कर देगा
    logout(request)  # session और user authentication clear हो जाएगी
    return redirect('login')  # redirect to login page या किसी और page पर


def singup_view(request):
    if request.method == "POST":
        form=  singupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # signup होते ही login करा देंगे
            return redirect('login')
    else:
        form = singupForm()
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

from .models import activity_schema

@login_required( login_url= 'login')
def selectActivity_view(request):
    activites =  activity_schema.objects.all()
    print(activites)
    return render(request, 'selectActivity.html', {'user': request.user, 'all_activities':activites})

# activites_slugify_map={ slugify(activite.activity_name): activite.activity_name for activite in activity_schema.objects.all()}

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
            record.activity_name = activity.activity_name
            record.save()
            messages.success(request, "Record saved successfully!")
            return redirect('viewRecord')
    else:
        form = userRecordsForm(activity)
        form.schema = activity

    return render(request, "record_form.html", {"form": form, "activity": activity, "messages": messages, 'user': request.user })



from .models import userRecords

@login_required(login_url= 'login')
def record_edit_view(request, record_id):
    record = get_object_or_404(userRecords, pk=record_id)
    activity = get_object_or_404(activity_schema, activity_name=record.activity_name)

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

    return render(request, 'record_form.html', {"form": form, "activity": activity, "messages": messages, 'user': request.user})



@login_required(login_url= 'login')
def viewRecordPage(request):
    records = userRecords.objects.filter(usr_id = request.user)
    # for record in records:
    #     data = { }
    data = records
    print(data)
#     data= Record.objects.filter(usr_id= user)
    return render(request, 'viewRecord.html', {'data': data, 'user': request.user })

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




# #chart views
# import json
# from django.db.models import Count
@login_required(login_url='login')
def chart_view(request):
    # user = myuser.objects.filter(user_id= request.user).first()
    records = userRecords.objects.filter(usr_id=request.user)

    data = {
        "chart1": sourceAnalize(records),
        "chart2": triggerReason(records),
        # "chart3": source_weekly_chart(user),
    #   "chart13":{
    #     'default_type':'pie',
    #     'chartTitle':'Test',
    #     "labels": ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    #     "data": [12, 19, 3, 5, 2, 3],
    # },   
    }
    return render(request, 'charts.html', {'chart_data': json.dumps(data), 'user': request.user})

# ''' chart releted function start '''


#Trigger reasion 
from collections import Counter
def sourceAnalize(records)->dict:
    # Initialize counter
    source_counter = Counter()

    for record in records:
        for source in record.source:
            source_counter[source] += 1

    # सभी source options को तय order में रखें
    all_sources = ['videos', 'books', 'comics', 'interction', 'chat']
    labels = all_sources
    data = [source_counter.get(source, 0) for source in all_sources]

    context = {
        'default_type':'bar',
        'chartTitle':'Source',
        'labels': labels,
        'data': data,
    }
    return context


def triggerReason(records)->dict:
    # Trigger reason counter
    trigger_counter = Counter()

    for record in records:
        for reason in record.trigger:
            trigger_counter[reason] += 1

    # All possible trigger reasons (order maintained)
    all_reasons = ['Digital visual', 'social interaction', 'hadNotDoFromLastLong']
    labels = all_reasons
    data = [trigger_counter.get(reason, 0) for reason in all_reasons]

    context = {
        'default_type':'pie',
        'chartTitle':'Trigger Reason',
        'labels': labels,
        'data': data,
    }
    return context

# from collections import defaultdict, Counter
# from django.utils.timezone import now
# import datetime
# def source_weekly_chart(user)->dict:
#     records = Record.objects.filter(usr_id=user).order_by('date')

#     # Step 1: group records by week number
#     week_source_data = defaultdict(Counter)
#     min_date = records.first().date if records.exists() else now().date()

#     for record in records:
#         week_diff = (record.date - min_date).days // 7
#         week_label = f"Week {week_diff + 1}"

#         for source in record.source:
#             week_source_data[week_label][source] += 1

#     # Step 2: Collect all weeks & sources
#     all_weeks = sorted(week_source_data.keys(), key=lambda x: int(x.split()[1]))
#     all_sources = ['videos', 'books', 'comics', 'interction', 'chat']

#     # Step 3: Prepare dataset format
#     datasets = []
#     for source in all_sources:
#         data = [week_source_data[week].get(source, 0) for week in all_weeks]

#         datasets.append({
#             'label': source,
#             'data': data
#         })
#     print(datasets)
#     context = {
#         'default_type':'line',
#         'chartTitle':'Source Weekly Chart',
#         'labels': all_weeks,
#         'datasets': datasets
#     }
#     return context
# ''' chart releted function end '''

# calander vies
# import calendar
# from datetime import datetime

# from django.shortcuts import render, redirect
from datetime import datetime
import calendar ,json
# from .models import Record  # अपने model को import करें

from bs4 import BeautifulSoup  # पहले ensure करें कि यह install है: pip install beautifulsoup4
@login_required(login_url='login')
def yearly_calendar(request, year=None):
    if year is None:
        year = datetime.now().year

    usr = request.session.get('user')
    user_records = userRecords.objects.filter(usr_id = request.user)
    record_dates = [rec.date for rec in user_records if rec.date.year == year]

    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    months = []
    months_json_data = []

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        html_month = cal.formatmonth(year, month)

        month_record_days = [d.day for d in record_dates if d.month == month]

        # ✅ अब HTML में marked days को class दो
        soup = BeautifulSoup(html_month, 'html.parser')
        for td in soup.find_all('td'):
            try:
                day = int(td.get_text(strip=True))
                if day in month_record_days:
                    td['class'] = td.get('class', []) + ['marked-day']
            except ValueError:
                pass  # Empty or non-numeric tds

        final_html_month = str(soup)

        months.append({
            'name': month_name,
            'html': final_html_month,
            'marked_days': month_record_days,
            'month_number': month,
        })

        months_json_data.append({
            'name': month_name,
            'marked_days': month_record_days,
            'month_number': month,
        })

    months_json_data = json.dumps(months_json_data)

    return render(request, 'calander.html', {
        'year': year,
        'months': months,
        'months_json': months_json_data, 
        'user': request.user,
    })


from django.http import JsonResponse
def userAccountManage(request, user_id=None, del_user_id=None):
    print(user_id, del_user_id)
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
