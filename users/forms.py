from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from users.models import User,Member

## User Login Form (Applied in member login)
class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']
        widgets = {
                '
        fields = ['email']
        widgets = {
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Member Profile Update Form
class MemberProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Member
        fields = ['member_profile_pic']
        
