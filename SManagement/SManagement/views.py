from django.shortcuts import render,redirect
from django.contrib.auth.models import User
def index(request):
    if request.session.has_key('is_viewer'):
        return redirect('/accounts')
    elif request.session.has_key('is_super'): 
        return redirect('/accounts')
    return render(request,'SManagement/index.html')