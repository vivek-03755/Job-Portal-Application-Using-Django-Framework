from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from hr.models import Hr
# Create your views here.

#common login screen
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:#if auth is successful
            login(request, user)#session/cookie set etc.
            if Hr.objects.filter(user=user).exists():
                return redirect('hrdash')
            return redirect('dash')
        else:
            msg = "Invalid Username or Password"
            return render(request,'authuser/login.html',{'msg':msg})
    return render(request,'authuser/login.html')


def candidateregister(request):
    return render(request,'authuser/candidateregister.html')

def hrregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword') 
        if password != cpassword:
            msg = "Password did't match"
            return render(request,'authuser/hrregister.html',{'msg':msg})
        user = User.objects.create_user(username=username, email=email, password=password)
        Hr(user=user).save()
        login(request, user) 
        return redirect('hrdash') 

    return render(request,'authuser/hrregister.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword') 
        if password != cpassword:
            msg = "Password did't match"
            return render(request,'authuser/hrregister.html',{'msg':msg})
        user = User.objects.create_user(username=username, email=email, password=password)
        
        login(request, user) 
        return redirect('dash')
    return render(request,'authuser/candidateregister.html')


def logoutUser(request):
    logout(request)
    return redirect('login')