from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.generic import  (View,TemplateView,
                                  ListView,DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from users.forms import UserForm,MemberProfileForm,MemberProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from users import models
from users.models import Member
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q


# For Member Sign Up
def MemberSignUp(request):
    user_type = 'member'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        member_profile_form = MemberProfileForm(data = request.POST)

        if user_form.is_valid() and member_profile_form.is_valid():

            user = user_form.save()
            user.is_member = True
            user.save()

            profile = member_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,member_profile_form.errors)
    else:
        user_form = UserForm()
        member_profile_form = MemberProfileForm()

    return render(request,'users/member_signup.html',{'user_form':user_form,'member_profile_form':member_profile_form,'registered':registered,'user_type':user_type})




## Sign Up page 
def SignUp(request):
    return render(request,'users/signup.html',{})

## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('users:login')
    else:
        return render(request,'users/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



## User Profile for member.
class MemberDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "member"
    model = models.Member
    template_name = 'users/member_detail_page.html'


## Profile update for members.
@login_required
def MemberUpdateView(request,pk):
    profile_updated = False
    member = get_object_or_404(models.Member,pk=pk)
    if request.method == "POST":
        form = MemberProfileUpdateForm(request.POST,instance=member)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'member_profile_pic' in request.FILES:
                profile.member_profile_pic = request.FILES['member_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = MemberProfileUpdateForm(request.POST or None,instance=member)
    return render(request,'users/member_update_page.html',{'profile_updated':profile_updated,'form':form})



class ClassMemberListView(LoginRequiredMixin,DetailView):
    model = models.Member
    template_name = "users/class_workers_list.html"
    context_object_name = "member"



##################################################################################################

## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('users:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'users/change_password.html',args)

