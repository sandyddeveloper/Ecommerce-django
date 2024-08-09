from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirmPassword = request.POST.get('confirmPassword')
        
        if password != confirmPassword:
            messages.warning(request, "Passwords do not match")
            return render(request, 'auth/signup.html')
        try:
            if User.objects.get(email=email):
                messages.warning(request, "User already exists")
                return render(request, 'auth/signup.html')
        except User.DoesNotExist:
            pass
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        messages.success(request, "Account created successfully")
        return redirect('/auth/login')  
    
    return render(request, 'auth/signup.html')
def handlelogin (request):
    return render(request, 'auth/login.html')