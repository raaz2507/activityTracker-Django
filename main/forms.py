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
         # --- Start < End time validation ---
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time must be earlier than end time.")


        # --- JSON conversion for source/trigger/extra ---
        schema = self.schema
        # Convert selected to True/False dict
        cleaned_data['source'] = {k: (k in cleaned_data.get('source', [])) for k in schema.source.keys()}
        cleaned_data['trigger'] = {k: (k in cleaned_data.get('trigger', [])) for k in schema.trigger.keys()}
        cleaned_data['extra'] = {k: (k in cleaned_data.get('extra', [])) for k in schema.extra.keys()}

        return cleaned_data


from .models import activity_schema
from django.forms.widgets import ColorInput


from django.core.exceptions import ValidationError
from PIL import Image

class ActivitySchemaForm(forms.ModelForm):
    color_field = forms.CharField(widget=ColorInput(attrs={'value':'#FFFFFF'}))

    class Meta:
        model = activity_schema
        fields = [
            'usr_id',
            'activity_name',
            'icon',
            'color_field',
            'source',
            'trigger',
            'extra'
        ]
        widgets = {
            'usr_id': forms.HiddenInput(),
            'activity_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter activity name'}),
            'source': forms.HiddenInput(),
            'trigger': forms.HiddenInput(),
            'extra': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['extra'].required = False

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if not icon:
            return None

        if hasattr(icon, 'name'):
            # SVG allow
            if icon.name.lower().endswith('.svg'):
                return icon

            # Other formats validate
            try:
                img = Image.open(icon)
                img.verify()  # corrupt image पकड़ेगा
            except Exception:
                raise ValidationError("Invalid or corrupted image file.")

            if img.format not in ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'WEBP']:
                raise ValidationError("Only PNG, JPG, GIF, BMP, TIFF, WebP or SVG images allowed...")

        return icon