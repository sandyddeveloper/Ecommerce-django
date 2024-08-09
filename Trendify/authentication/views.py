from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        password = request.POST['password']
        email = request.POST['email']
        confirmPassword = request.POST['confirmPassword']
        
        if password != confirmPassword:
            messages.warning(request, "Passwords do not match")
            return render(request, 'auth/signup.html')
        try:
            if User.objects.filter(username=email):
                messages.warning(request, "User already exists")
                return render(request, 'auth/signup.html')
        except Exception as identifier:
            pass
        myuser = User.objects.create_user( email, email, password)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        messages.success(request, "Account created successfully")
        return redirect('/auth/login')  
    
    return render(request, 'auth/signup.html')

def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['email']
        userpassword = request.POST['password']
        
        myuser = authenticate(username=username, password=userpassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login successful")
            return render(request,'index.html')  
        else:
            messages.warning(request, "Invalid credentials")
            return redirect('/auth/login')  
    
    return render(request, 'auth/Login.html')
