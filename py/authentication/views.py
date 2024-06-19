from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from resoulse import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import datetime
from authentication.models import ClockInTime

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

@login_required(login_url='/signin')
def about(request):
    return render(request, "authentication/about.html")

@login_required(login_url='/signin')
def profile(request):
    fname = request.user.first_name 
    return render(request, "authentication/profile.html", {'fname': fname})
    

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please use another username.")
        
        elif User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
        
        elif len(username)>10:
            messages.error(request, "Username must be under 10 Characters!")

        elif pass1!=pass2:
            messages.error(request, "Passwords did not match!")
        
        elif not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request, "Your Account has been successfully created.")
        
        
            return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "authentication/signin.html")
    else:
        return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("home")

@login_required(login_url='/signin')
def clocked(request):
    
    if request.method == 'POST':
        # Create a new ClockInTime instance and save it to the database
        clock_in_time = ClockInTime.objects.create()
        return redirect('clocked')  # Redirect to the same page after clocking in
    return render(request, "authentication/clocked.html")
    
@login_required(login_url='/signin')
def clockview(request):
    clock_in_time = ClockInTime.objects.last()  # Retrieve the latest ClockInTime instance
    return render(request, "authentication/clockview.html", {'clock_in_time': clock_in_time})
    

