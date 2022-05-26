from email import message
from email.message import EmailMessage
from errno import EKEYEXPIRED
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib import auth
# Create your views here.
#activation imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def login(request):
     
    if request.method =='POST':
        
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)
       
        if user is not None:
            
            auth.login(request,user)
            messages.success(request,'you are logged in...')
            return redirect('dashboard')
        else:
            
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username =email.split('@')[0]
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
            )
            user.phone_number = phone_number
            user.save()

            #account activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            message= render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_mail = email
            send_email = EmailMessage(mail_subject,message,to=[to_mail])
            send_email.send()

            messages.success(request,'Registration successful...')
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()


    return render(request,'accounts/register.html',{'form':form})

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Logged out successful')
    return redirect('login')


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._base_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None 

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'Congrats !! Your account activated ')
        return redirect('login')
    else:
        messages.error(request,'Invalid activate link')
        return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request,'base/dashboard.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user =Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message= render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_mail = email
            send_email = EmailMessage(mail_subject,message,to=[to_mail])
            send_email.send()

            messages.success(request,'Password reset email has been sent successfully to your mail ')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgot_password')
    return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._base_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None 

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'Invaild link')
        return redirect('login')
    

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid =request.session.get('uid')
            user =Account.objects.get(pk=uid)
            print(user)
            user.set_password(password)
            user.save()
            print(user.password)
            messages.success(request,'Password changed successfully !!!')
            return redirect('login')
        else:
            messages.error(request,'Password does not match ')
            return redirect('resetpassword')

    return render(request,'accounts/resetpassword.html')
