from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import token_generator, EmailThread
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import Product,Category

# Create your views here.
def Home (request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirmPassword = request.POST.get('confirmPassword')

        # Gather potential errors
        errors = []
        if password != confirmPassword:
            errors.append("Passwords do not match.")
        
        if User.objects.filter(username=email).exists():
            errors.append("User already exists.")

        if errors:
            for error in errors:
                messages.warning(request, error)
            return render(request, 'Auth/signup.html')

        # Create the user if there are no errors
        myuser = User.objects.create_user(email, email, password)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.is_active = False  # Deactivate account until it is confirmed
        myuser.save()

        # Send activation email
        current_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message = render_to_string('Auth/activate.html', {
            'user': myuser,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': token_generator.make_token(myuser),
        })

        email_message = EmailMessage(
            email_subject, message, settings.EMAIL_HOST_USER, [email]
        )
        EmailThread(email_message).start()
        messages.info(request, "Activate your account by clicking the link sent to your email.")
        return redirect('handlelogin')

    return render(request, 'Auth/signup.html')


def about_view(request):
    return render(request, 'about.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated. You can now login.")
            return redirect('handlelogin')
        else:
            messages.error(request, "Activation link is invalid!")
            return render(request, 'Auth/activatefail.html')


def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['email']
        userpassword = request.POST['password']
        
        myuser = authenticate(username=username, password=userpassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login successful")
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            messages.warning(request, "Invalid credentials")
            return redirect('handlelogin')  
    else:
        return render(request, 'Auth/login.html')


def handlelogout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/')


def dashboard(request):
    # Fetch all products and order them by category name
    products = Product.objects.all().order_by('category__name')
    
    # Get distinct categories
    categories = products.values('category__name', 'category_id').distinct()

    # Group products by category
    products_by_category = {}
    for category in categories:
        category_name = category['category__name']
        products_in_category = products.filter(category_id=category['category_id'])
        products_by_category[category_name] = products_in_category
    
    context = {
        'products_by_category': products_by_category,
    }
    return render(request, 'dashboard.html', context)
class RequestResetEmailView(View):
    def get(self, request):
            return render(request, 'Auth/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)
        
        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset Your Password]'
            message = render_to_string('Auth/reset-user-password.html',
            {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            })    
        
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            EmailThread(email_message).start()
            
            messages.info(request,"We Have Sent You An Email With Instructions on How to Rest the Password")
            return render(request, 'Auth/request-reset-email.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token ):
        context ={
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link in Invalid")
                return render(request,'Auth/request-reset-email.html')
            
        except DjangoUnicodeDecodeError as identifier:
            pass
        
        return render(request,'Auth/reset-new-password.html', context)
    
    def post(self, request, uidb64, token):
        context ={
            'uidb64': uidb64,
            'token': token
        }
        
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if password!= confirmPassword:
            messages.warning(request, "Passwords do not match")
            return render(request,'Auth/reset-new-password.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password successfully reset. Please log in with the new password")
            return redirect('handlelogin')
        
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Something Went Wrong")
            return render(request,'Auth/reset-new-password.html', context)
        
           

def product_view(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request,nun):
    # Replace Hyphens with Space characters
    nun = nun.replace('-',' ')
    #Grab the category from the url
    try:
        #Look Up to Category
        category = Category.objects.get(name = nun)
        # Get all products in this category
        products = Product.objects.filter(category=category)
        # Render the products in this category
        return render(request, 'category.html', {'products': products, 'category': category})
        
    except:
        messages.success(request, "That's not a valid category")
        return redirect('dashboard')
    
def update_user(request):
    return render(request, 'update_user.html')