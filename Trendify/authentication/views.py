# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# # to active the user by providing the mail to the user t verify their account
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.urls import NoReverseMatch, reverse
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes,  DjangoUnicodeDecodeError

# #getting tokens from utils.py in auth folder
# from .utils import TokenGenerator

# # for sending emails to user for verifications
# from django.core.mail import send_mail,EmailMultiAlternatives
# from django.core.mail import BadHeaderError,send_mail
# from django.core.mail import EmailMessage

# #to send the "TO" address and from for mailing for users
# from django.conf import settings

# #to generate tokens for user 





# def signup(request):
#     if request.method == 'POST':
#         firstName = request.POST['firstName']
#         lastName = request.POST['lastName']
#         password = request.POST['password']
#         email = request.POST['email']
#         confirmPassword = request.POST['confirmPassword']
        
#         if password != confirmPassword:
#             messages.warning(request, "Passwords do not match")
#             return render(request, 'auth/signup.html')
#         try:
#             if User.objects.filter(username=email):
#                 messages.warning(request, "User already exists")
#                 return render(request, 'auth/signup.html')
#         except Exception as identifier:
#             pass
#         myuser = User.objects.create_user( email, email, password)
#         myuser.first_name = firstName
#         myuser.last_name = lastName
#         myuser.save()
#         current_site = get_current_site(request)
#         email_subject = "Activate Your Account"
#         message=render_to_string('auth/activate.html', {
#             'user': myuser,
#             'domain':"127.0.0.1:8000" ,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': token_generator.make_token(myuser),
#         })
        
#         email_message = EmailMessage(email_subject, message.settings.EMAIL_HOST_USER, [email],)
#         EmailThread(email_message).start()
#         messages.info(request, "Activate Your Account By Clicking This Link On Your Email") 
#         return redirect('/auth/login')  
    
#     return render(request, 'auth/signup.html')

# def handlelogin(request):
#     if request.method == 'POST':
#         username = request.POST['email']
#         userpassword = request.POST['password']
        
#         myuser = authenticate(username=username, password=userpassword)
        
#         if myuser is not None:
#             login(request, myuser)
#             messages.success(request, "Login successful")
#             return render(request,'dashboard.html')  
#         else:
#             messages.warning(request, "Invalid credentials")
#             return redirect('/auth/login')  
    
#     return render(request, 'auth/Login.html')


# def handlelogout(request):
#     logout(request)
#     messages.success(request, "Logged out successfully")
#     return redirect('/auth/login')

# def dashboard(request):
#     return render(request,'dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError

from .utils import TokenGenerator  

from django.core.mail import EmailMessage
from django.conf import settings

import threading

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

token_generator = TokenGenerator()  

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
        
        if User.objects.filter(username=email).exists():
            messages.warning(request, "User already exists")
            return render(request, 'auth/signup.html')

        myuser = User.objects.create_user(email, email, password)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        
        current_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message = render_to_string('auth/activate.html', {
            'user': myuser,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': token_generator.make_token(myuser),
        })
        
        email_message = EmailMessage(
            email_subject, message, settings.EMAIL_HOST_USER, [email]
        )
        EmailThread(email_message).start()
        messages.info(request, "Activate Your Account By Clicking The Link Sent To Your Email") 
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
            return redirect('dashboard.html')  # Use the named URL
        else:
            messages.warning(request, "Invalid credentials")
            return redirect('/auth/login')  
    
    return render(request, 'auth/login.html')

def handlelogout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/auth/login')

def dashboard(request):
    return render(request, 'dashboard.html')
