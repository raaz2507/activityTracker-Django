from django import forms
from .models  import myuser, userRecords

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.forms import AuthenticationForm

class loginForm(AuthenticationForm):
    pass
    # class Meta:
    #     model = myuser
    #     fields = ['username', 'password']

class BaseUserForm(forms.ModelForm):
    field_groups = [
        ('name', ['first_name', 'last_name']),  # group1
    ]
    class Meta:
        model = myuser
        fields = ['username','first_name', 'last_name',  'email', 'phone', 'gender', 'age']
        widgets= {
            'gender' : forms.RadioSelect(attrs={ "class" : "radio_btn",}),
            "username": forms.TextInput(attrs= {'placeholder': "User Name"}),
            "first_name": forms.TextInput(attrs= {'placeholder': "First Name"}),
            "last_name": forms.TextInput(attrs= {'placeholder': "Last Name"}),
            "email": forms.EmailInput(attrs= {'placeholder': "Email"}),
        }

class SignUpForm(UserCreationForm, BaseUserForm):
    class Meta(BaseUserForm.Meta, UserCreationForm.Meta):
        fields = BaseUserForm.Meta.fields + ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            "placeholder": "Enter password",
            "minlength": "4",
            "maxlength": "6",
        })
        self.fields['password2'].widget.attrs.update({
            "placeholder": "Confirm password",
            "minlength": "4",
            "maxlength": "6",
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user

class UserUpdateForm(UserChangeForm, BaseUserForm):
    password = forms.CharField(
        required = False, 
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label= "Confirm Password"
    )

    class Meta(BaseUserForm.Meta, UserChangeForm.Meta):
        fields = BaseUserForm.Meta.fields + ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self.add_error('confirm_password', "Password aur Confirm Password match nahi kar rahe!")
        return cleaned_data


# class singupForm(UserCreationForm):
#     class Meta:
#         model =myuser
#         fields = ['username','first_name', 'last_name',  'email', 'phone', 'gender', 'age', 'password1', 'password2']
#         widgets= {
#             'gender' : forms.RadioSelect(attrs={ "class" : "radio_btn",}),
#             "username": forms.TextInput(attrs= {'placeholder': "User Name"}),
#             "first_name": forms.TextInput(attrs= {'placeholder': "First Name"}),
#             "last_name": forms.TextInput(attrs= {'placeholder': "Last Name"}),
#             "email": forms.EmailInput(attrs= {'placeholder': "Email"}),
#         }
#     def __init__(self, *args, **kwargs):
#         super().__init__( *args, **kwargs)

#         # force attributes in password1
#         self.fields['password1'].widget.attrs.update({
#             "placeholder": "Enter password",
#             "minlength": "4",
#             "maxlength": "6",
#         })

#         # force attributes in password2
#         self.fields['password2'].widget.attrs.update({
#             "placeholder": "Confirm password",
#             "minlength": "4",
#             "maxlength": "6",
#         })

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_staff = False
#         user.is_superuser = False
#         if commit:
#             user.save()
#         return user
# # Option 2: अगर password भी update करना चाहते हैं (optional)
# from django.contrib.auth.forms import UserChangeForm
# class UserUpdateForm(UserChangeForm):
#     password = forms.CharField(
#         required = False, 
#         widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
#         label='Password'
#         )
#     confirm_password = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
#         label= "Confirm Password"
#         )

#     class Meta:
#         model = myuser
#         fields = ['username','first_name', 'last_name',  'email', 'phone', 'gender', 'age', 'password']
#         widgets= {
#             'gender' : forms.RadioSelect(attrs={ "class" : "radio_btn",}),
#             "username": forms.TextInput(attrs= {'placeholder': "User Name"}),
#             "first_name": forms.TextInput(attrs= {'placeholder': "First Name"}),
#             "last_name": forms.TextInput(attrs= {'placeholder': "Last Name"}),
#             "email": forms.EmailInput(attrs= {'placeholder': "Email"}),
#         }
    
#     def clean(self):
#         cleaned_data = super().clean()
#         password =  cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password and password!= confirm_password:
#             self.add_error('confirm_password', "Password aur Confirm Password match nahi kar rahe!")
        
#         return cleaned_data



from .models import userRecords, activity_schema

class userRecordsForm(forms.ModelForm):
    def __init__(self, activity_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        schema = activity_instance  # activity_schema object directly

        self.fields['source'] = forms.MultipleChoiceField(
            choices=[(key, key) for key in schema.source.keys()],
            widget=forms.CheckboxSelectMultiple,
            required=False
        )
        self.fields['trigger'] = forms.MultipleChoiceField(
            choices=[(key, key) for key in schema.trigger.keys()],
            widget=forms.CheckboxSelectMultiple,
            required=False
        )
        self.fields['extra'] = forms.MultipleChoiceField(
            choices=[(key, key) for key in schema.extra.keys()],
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

    class Meta:
        model = userRecords
        fields = ['date', 'start_time', 'end_time', 'source', 'trigger', 'extra']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # activity_instance schema अब view से pass किया जाएगा
        schema = self.schema

        # Convert selected to True/False dict
        cleaned_data['source'] = {k: (k in cleaned_data.get('source', [])) for k in schema.source.keys()}
        cleaned_data['trigger'] = {k: (k in cleaned_data.get('trigger', [])) for k in schema.trigger.keys()}
        cleaned_data['extra'] = {k: (k in cleaned_data.get('extra', [])) for k in schema.extra.keys()}

        return cleaned_data