from django import forms
from .models import Users, Record

class usersForm(forms.ModelForm):
    
    class Meta:
        model =  Users
        # fields: '__all__'
        fields = ['user_name', 'pwd']
    
    labels={
        'user_name': 'User Name',
        'pwd': "Password",
    }

    widgets ={
        'user_name': forms.TextInput(attrs={'type':'text', 'class':'', 'placeholder': 'Enter User Name'}),
        'pwd': forms.PasswordInput(attrs={'type': 'password','class': '', 'placeholder': 'Enter Your password'})
    }
class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=100, label="User Name: ", widget=forms.TextInput(attrs={'placeholder': 'Enter User Name'}))
    pwd = forms.CharField(label="password: ", widget=forms.PasswordInput(attrs={'type':'password', 'placeholder': 'Enter Password'}))

class recordForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = '__all__'
        exclude = ['usr_id']
        labels={
            'date': "Date",
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'source': 'Source',
            'trigger_reason': 'Trigger Reasion',
            'timesCount': 'Times'
        }
        widgets={
            'usr_id': forms.HiddenInput(attrs={'type':'hidden'}),
            'date' : forms.DateInput(attrs={'type': 'date','class':''}),
            'start_time' : forms.TimeInput(attrs={'type': 'time', 'class': ''}),
            'end_time' : forms.TimeInput(attrs={'type': 'time', 'class': ''}),
            'source': forms.CheckboxSelectMultiple(attrs={'type':'checkbox', 'class': '', 'style': ''}),
            'trigger_reason':forms.CheckboxSelectMultiple(attrs={'type':'checkbox', 'class':'', 'style':''}),

        }
