from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
# Create your views here.

def index(request):
    if request.session.has_key('is_super'):
        all_users = User.objects.all()
        return render(request,'accounts/adminLogin.html',{'all_users':all_users})
    elif request.session.has_key('is_viewer'):
        return render(request,'accounts/viewerLogin.html')
    return redirect('/')

def addUser(request):

    if request.method == "POST":
        #get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        emailSignup = request.POST['emailSignup']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for errorneous inputs
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already taken please choose some other username')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if len(username)>10:
            messages.error(request, 'Username must be under 10 characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if not username.isalnum():
            messages.error(request,'Username must only contain alpha numeric characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


        #Create the user
        myuser = User.objects.create_user(username,emailSignup,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'Your account has been successfully created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    if request.session.has_key('is_super'):
        return render(request,'accounts/addUser.html')
    return redirect('/')


def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully logged out')
    return redirect('/')

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('/')
        if request.user.is_superuser:
            all_users = User.objects.all()
            request.session['is_super'] = True
            return render(request,'accounts/adminLogin.html',{'all_users':all_users})
        else:
            request.session['is_viewer'] = True
        return render(request,'accounts/viewerLogin.html',{'user':request.user})
    else:
        return redirect('/')
