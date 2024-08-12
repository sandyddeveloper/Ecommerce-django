# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.views.generic import View
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.urls import reverse
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_str,DjangoUnicodeDecodeError
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .utils import token_generator, EmailThread
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from .models import Product
# from math import ceil
# from authentication import keys

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
        
#         if User.objects.filter(username=email).exists():
#             messages.warning(request, "User already exists")
#             return render(request, 'auth/signup.html')

#         myuser = User.objects.create_user(email, email, password)
#         myuser.first_name = firstName
#         myuser.last_name = lastName
#         myuser.is_active = False  # Deactivate account until it is confirmed
#         myuser.save()
        
#         current_site = get_current_site(request)
#         email_subject = "Activate Your Account"
#         message = render_to_string('Auth/activate.html', {
#             'user': myuser,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': token_generator.make_token(myuser),
#         })
        
#         email_message = EmailMessage(
#             email_subject, message, settings.EMAIL_HOST_USER, [email]
#         )
#         EmailThread(email_message).start()
#         messages.info(request, "Activate your account by clicking the link sent to your email.") 
#         return redirect('/auth/login')  
    
#     return render(request, 'auth/signup.html')


# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
        
#         if user is not None and token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, "Your account has been activated. You can now login.")
#             return redirect('/auth/login')
#         else:
#             messages.error(request, "Activation link is invalid!")
#             return render(request, 'Auth/activatefail.html')


# def handlelogin(request):
#     if request.method == 'POST':
#         username = request.POST['email']
#         userpassword = request.POST['password']
        
#         myuser = authenticate(username=username, password=userpassword)
        
#         if myuser is not None:
#             login(request, myuser)
#             messages.success(request, "Login successful")
#             return redirect('dashboard')  # Redirect to the dashboard
#         else:
#             messages.warning(request, "Invalid credentials")
#             return redirect('/auth/login')  
    
#     return render(request, 'auth/login.html')


# def handlelogout(request):
#     logout(request)
#     messages.success(request, "Logged out successfully")
#     return redirect('/')


# def dashboard(request):
#     current_user = request.user
#     print(current_user)
#     allProds = []
#     catprods = Product.objects.values('category', 'id')
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         prod = Product.objects.filter(category=cat)
#         n=len(prod)
#         nSlides = n // 4 + ceil((n / 4 ) - (n // 4))
#         allProds.append([prod, range(1, nSlides), nSlides])
        
#     params = {'allProds':allProds}
#     return render(request, 'dashboard.html',params)


# class RequestResetEmailView(View):
#     def get(self, request):
#             return render(request, 'Auth/request-reset-email.html')

#     def post(self, request):
#         email = request.POST['email']
#         user = User.objects.filter(email=email)
        
#         if user.exists():
#             current_site = get_current_site(request)
#             email_subject = '[Reset Your Password]'
#             message = render_to_string('Auth/reset-user-password.html',
#             {
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
#                 'token': PasswordResetTokenGenerator().make_token(user[0])
#             })    
        
#             email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
#             EmailThread(email_message).start()
            
#             messages.info(request,"We Have Sent You An Email With Instructions on How to Rest the Password")
#             return render(request, 'Auth/request-reset-email.html')


# class SetNewPasswordView(View):
#     def get(self, request, uidb64, token ):
#         context ={
#             'uidb64': uidb64,
#             'token': token
#         }
#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=user_id)
            
#             if not PasswordResetTokenGenerator().check_token(user,token):
#                 messages.warning(request,"Password Reset Link in Invalid")
#                 return render(request,'Auth/request-reset-email.html')
            
#         except DjangoUnicodeDecodeError as identifier:
#             pass
        
#         return render(request,'Auth/set-new-password.html', context)
    
#     def post(self, request, uidb64, token):
#         context ={
#             'uidb64': uidb64,
#             'token': token
#         }
        
#         password = request.POST['password']
#         confirmPassword = request.POST['confirmPassword']
#         if password!= confirmPassword:
#             messages.warning(request, "Passwords do not match")
#             return render(request,'Auth/set-new-password.html', context)
        
#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=user_id)
#             user.set_password(password)
#             user.save()
#             messages.success(request, "Password successfully reset. Please log in with the new password")
#             return redirect('/auth/login')
        
#         except DjangoUnicodeDecodeError as identifier:
#             messages.error(request, "Something Went Wrong")
#             return render(request,'Auth/set-new-password.html', context)
        
           

# def checkout(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "Login is not authenticated")
#         return redirect('/auth/login')
#     if request.method == 'POST':
#         items_json = request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount = request.POST.get('amount', '')
#         email = request.POST.get('email', '')
#         address1 = request.POST.get('address1', '')
#         address2 = request.POST.get('address2', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zipcode = request.POST.get('zipcode', '')
#         phone = request.POST.get('phone', '')
        
#         Order = Order(items_json, name=name, amount=amount, email=email, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode, phone=phone)
#         print(amount)
#         Order.save()
#         update = OrderUpdate(order_id=Order.order_id, update_desc='the order has been placed')
#         update.save()
#         thank = True
#         id = Order.order_id
#         oid = str(id)+"Trendify"
#         param_dict = {
#             'MID' : 'MID',
#             'ORDER_ID' : oid,
#             'TXN_AMOUNT' : str(amount),
#             'CUST_ID' : email,
#             'WEBSITE' : 'WEBSTAGING',
#             'CHANNEL_ID' : 'WEB',
#             'INDUSTRY_TYPE_ID' : 'Retail',
#             'CALLBACK_URL' : 'http://127.0.0.1:8000/handlerequest',
#         }
#         param_dict['CHECKSUMHASH'] =Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#         return render(request, 'payment.html',{'param_dict':param_dict})
#     return render(request, 'checkout.html')

# # @csrf_exempt
# # def handlerequest(request):
    
# #     # paytm will send you post request here to pay
# #     form = request.POST
# #     response_dict = {}
# #     for i in form.keys():
# #         response_dict[i] = form[i]
# #         if i == 'CUST_ID' or i == 'CHECKSUMHASH':
# #             checksum = form[i]
            
# #     verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY, checksum)
# #     if verify:
# #         if response_dict['RESPCODE'] == '01':











# # from django.shortcuts import render, redirect
# # from django.contrib.auth.models import User
# # from django.contrib.auth import authenticate, login, logout
# # from django.contrib import messages

# # # to active the user by providing the mail to the user t verify their account
# # from django.contrib.sites.shortcuts import get_current_site
# # from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# # from django.urls import NoReverseMatch, reverse
# # from django.template.loader import render_to_string
# # from django.utils.encoding import force_bytes,  DjangoUnicodeDecodeError

# # #getting tokens from utils.py in auth folder
# # from .utils import TokenGenerator

# # # for sending emails to user for verifications
# # from django.core.mail import send_mail,EmailMultiAlternatives
# # from django.core.mail import BadHeaderError,send_mail
# # from django.core.mail import EmailMessage

# # #to send the "TO" address and from for mailing for users
# # from django.conf import settings

# #resetpassword generators
# #from django.contrib.auth.tokens import PasswordResetTokenGenerator