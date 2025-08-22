from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import usersForm, LoginForm, recordForm
from .models import Users, Record


def home(request):
    return redirect('login')



from django.contrib.auth.hashers import make_password

from django.contrib import messages

def singup(request):
    success = False

    if request.method == "POST":
        usr_name = request.POST.get("usr_name")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")

        # Password check
        if pwd != cpwd:
            messages.error(request, "Passwords do not match")
            return render(request, "singup.html", {'success': False})

        # Check username already exists
        if Users.objects.filter(user_name=usr_name).exists():
            messages.error(request, "Username already exists")
            return render(request, "singup.html", {'success': False})

        # Save user
        # hashed_pwd = make_password(pwd)
        # Users(user_name=usr_name, pwd=hashed_pwd).save()
        Users(user_name=usr_name, pwd = pwd).save()
        success = True
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, "singup.html", {'success': success})

# def singup(request):
#     form = usersForm()
#     print('form1')
#     success = False
#     if request.method == "POST":
#         print('form2')
#         form =  usersForm(request.POST)
#         if form.is_valid():
#             print('form3')
#             usr_name =  request.POST.get("usr_name")
#             pwd = request.POST.get("pwd")
#             cpwd = request.POST.get("cpwd")
#             print(f'{usr_name} - {pwd} - {cpwd}')
#             if pwd != cpwd:
#                 form.add_error(None, "Passwords do not match")
#                 return render(request, "singup.html", {'form': form, 'success': False})
#             Users(user_name= usr_name , pwd = pwd).save()
            
#             # form.save()
#             success=True
            
#             return redirect('login')
#         else:
#             form = usersForm()
#     return render(request, "singup.html",{'form':form, 'success': success})

# from django.contrib import messages

def login(request):
    success = True
    usrName = psswd= ''
    if request.method == "POST":
        usrName = request.POST.get("userName")
        psswd = request.POST.get("pwd")

       
        user =  Users.objects.filter(user_name = usrName, pwd = psswd).first()
        if user:
            request.session['usr_id'] = user.usr_id
            return redirect('addRecord')  # apne home URL ka naam daalo yahan
        else:
            messages.error(request, "Username not exists or password does not match")
            success= False
    return render(request, "login.html",{ 'userName':usrName, 'password':psswd , 'success': success}) 
# def login(request):
#     form = LoginForm()
#     success = True

#     if request.method == "POST":
        
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             usrName = form.cleaned_data.get('user_name')
#             psswd = form.cleaned_data.get('pwd')
#             print(f"{usrName} {psswd}")
#             user =  Users.objects.filter(user_name = usrName, pwd = psswd).first()
#             if user:
#                 request.session['usr_id'] = user.usr_id
#                 # request.session["userName"] = usrName
#                 # request.session["pwd"] = pwd
                
#                 return redirect('addRecord')
#             else:
#                 success= False
#                 form = LoginForm()
#     return render(request, 'login.html', {'form':form, 'success': success})

def logout( request ):
    request.session['usr_id']=''
    return redirect('home')

def viewRecordPage(request):
    usr_id = request.session.get('usr_id')
    if not usr_id:
        return redirect('login')
    user = Users.objects.filter(usr_id= usr_id).first()
    print(user)
    data= Record.objects.filter(usr_id= user)
    print(data)
    return render(request, 'viewRecord.html', {'data': data})


# def addRecordPage(request):
#     if request.method == "POST":
#         form = recordForm(request.POST)
#         if form.is_valid():
            
#             instance = form.save(commit=False)
#             usr_id = request.session.get('usr_id')
#             if usr_id:
#                 usr= Users.objects.get(usr_id =  usr_id)
#                 instance.usr_id = usr
#                 instance.save()
#                 # form.save_m2m()  # अब source (ManyToMany) save करो
#             return redirect('viewRecord')
#     else:
#         form = recordForm()
    
#     return render(request, 'addRecord.html', {'form': form})


#create and update dono ke liye
def RecordFormPage(request, id=None):
    if not request.session.get('usr_id'):
        return redirect('login')


    if id:
        row= get_object_or_404(Record, pk=id)
    else:
        row= None
    
    form = recordForm(request.POST or None, instance= row)

    if form.is_valid():
        instance = form.save(commit=False)
        usr_id = request.session.get('usr_id')
        if usr_id:
            usr= Users.objects.get(usr_id =  usr_id)
            instance.usr_id = usr
            instance.save()
            # form.save_m2m()  # अब source (ManyToMany) save करो
        return redirect('viewRecord')
    return render(request, 'addRecord.html', {'form':form})

def record_delete(request, id=None):
    row= get_object_or_404(Record, pk=id)
    if request.method=="POST":
        row.delete();
        return redirect('viewRecord')

#chart views
import json
from django.db.models import Count

def chart_view(request):
    usr_id = request.session.get('usr_id')
    if not usr_id:
        return redirect('login')

    user = Users.objects.filter(usr_id= usr_id).first()
    records = Record.objects.filter(usr_id=user)

    data = {"chart1": sourceAnalize(records),
    "chart2": triggerReason(records),
    "chart3": source_weekly_chart(user),
    # "chart13":{
    #     'default_type':'pie',
    #     'chartTitle':'Test',
    #     "labels": ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    #     "data": [12, 19, 3, 5, 2, 3],
    # },   
    }
    return render(request, 'charts.html', {'chart_data': json.dumps(data)})

''' chart releted function start '''


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
        for reason in record.trigger_reason:
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

from collections import defaultdict, Counter
from django.utils.timezone import now
import datetime
def source_weekly_chart(user)->dict:
    records = Record.objects.filter(usr_id=user).order_by('date')

    # Step 1: group records by week number
    week_source_data = defaultdict(Counter)
    min_date = records.first().date if records.exists() else now().date()

    for record in records:
        week_diff = (record.date - min_date).days // 7
        week_label = f"Week {week_diff + 1}"

        for source in record.source:
            week_source_data[week_label][source] += 1

    # Step 2: Collect all weeks & sources
    all_weeks = sorted(week_source_data.keys(), key=lambda x: int(x.split()[1]))
    all_sources = ['videos', 'books', 'comics', 'interction', 'chat']

    # Step 3: Prepare dataset format
    datasets = []
    for source in all_sources:
        data = [week_source_data[week].get(source, 0) for week in all_weeks]

        datasets.append({
            'label': source,
            'data': data
        })
    print(datasets)
    context = {
        'default_type':'line',
        'chartTitle':'Source Weekly Chart',
        'labels': all_weeks,
        'datasets': datasets
    }
    return context
''' chart releted function end '''

# calander vies
import calendar
from datetime import datetime

from django.shortcuts import render, redirect
from datetime import datetime
import calendar
from .models import Record  # अपने model को import करें

from bs4 import BeautifulSoup  # पहले ensure करें कि यह install है: pip install beautifulsoup4

def yearly_calendar(request, year=None):
    if not request.session.get('usr_id'):
        return redirect('login')

    if year is None:
        year = datetime.now().year

    usr_id = request.session.get('usr_id')
    user_records = Record.objects.filter(usr_id__usr_id=usr_id)
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
        'months_json': months_json_data
    })

from django.http import JsonResponse
def userAccountManage(request, user_id=None, del_user_id=None):
    print(user_id, del_user_id)
    if del_user_id:
        user = get_object_or_404(Users, usr_id = del_user_id)
        # user.delete()
        userAccData = list(Users.objects.all().values('usr_id','user_name', 'pwd' ))
        return JsonResponse({'userAccData':userAccData, 'messages':{'tag':"sussess", 'msg':f"{del_user_id} data Sussefuy Deleted..."}}, safe=False)
    if user_id:
        userData = list(Record.objects.filter(usr_id__usr_id=user_id).values( 'usr_id','date', 'start_time', 'end_time', 'source', 'trigger_reason', 'timesCount'))
        return JsonResponse(userData, safe=False);
    else:
        userAccounts = Users.objects.all()
        return render(request, 'userAccountManage.html', {'userAcounts': userAccounts})

def userAccountManageDeleteUsr(request, user_id):
    user = get_object_or_404(Users, usr_id=user_id);
    user.delete();

# import json
# def yearly_calendar(request, year=None):
#     if not request.session.get('usr_id'):
#         return redirect('login')

#     if year is None:
#         year = datetime.now().year

#     usr_id = request.session.get('usr_id')
#     user_records = Record.objects.filter(usr_id__usr_id=usr_id)
#     record_dates = [rec.date for rec in user_records if rec.date.year == year]

#     cal = calendar.HTMLCalendar(calendar.SUNDAY)
#     months = []
#     months_json_data = []

#     for month in range(1, 13):
#         month_name = calendar.month_name[month]
#         html_month = cal.formatmonth(year, month)

#         month_record_days = [d.day for d in record_dates if d.month == month]

#         months.append({
#             'name': month_name,
#             'html': html_month,
#             'marked_days': month_record_days,
#             'month_number': month,
#         })

#         months_json_data.append({
#             'name': month_name,
#             'marked_days': month_record_days,
#             'month_number': month,
#         })

#     # ✅ json.dumps बाहर करो
#     months_json_data = json.dumps(months_json_data)

#     return render(request, 'calander.html', {
#         'year': year,
#         'months': months,
#         'months_json': months_json_data
#     })


# def yearly_calendar(request, year=None):
#     if not request.session.get('usr_id'):
#         return redirect('login')

        
#     if year is None:
#         year = datetime.now().year

#     cal = calendar.HTMLCalendar(calendar.SUNDAY)
#     months = []

#     for month in range(1, 13):
#         month_name = calendar.month_name[month]
#         html_month = cal.formatmonth(year, month)
#         months.append({'name': month_name, 'html': html_month})

#     return render(request, 'calander.html', {'year': year, 'months': months})
