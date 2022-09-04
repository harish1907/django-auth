from ast import Pass
from email.message import Message
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login as df_login, logout, authenticate, update_session_auth_hash
from django.contrib import messages

# Create your views here.
def signupform(request):
    if request.method == "POST":
        fm = UserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            fm = UserCreationForm()
    else:
        fm = UserCreationForm()
    return render(request, "index.html", {"form": fm})

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data["username"]
                upass = fm.cleaned_data["password"]
                print(fm.cleaned_data)
                user = authenticate(request, username=uname, password=upass)
                if user is not None:
                    df_login(request, user)
                    messages.success(request, "welcome to profile page you complete login....")
                    return HttpResponseRedirect("/profile/")
        fm = AuthenticationForm()
        return render(request, "login.html", {"form": fm})
    return HttpResponseRedirect("/profile/")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html", {"name": request.user})
    return HttpResponseRedirect("/login/")

def logoutpage(request):
    logout(request)
    return HttpResponseRedirect("/login/")


# change password with old password
def changepass_with_oldpass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data = request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, user=fm.user)
                return HttpResponseRedirect("/profile/")
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'changepass.html', {"form": form})
    return HttpResponseRedirect("/login/")