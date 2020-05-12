from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from .models import *


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('Users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'Users/Signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request,'Users/login.html')
    else:
        return HttpResponse('Activation link is invalid!')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = form.get_user()
            login(request, user)
        if next in request.POST:
            return render(request.GET['next'])
        else:   
            return render('Main-Site/index.html')
    else:
        form = AuthenticationForm()   
    return render(request, 'Users/login.html',{'form': form})

def logout_view(request):
   logout(request)
   return render(request,'Main-Site/index.html')

def add_notes(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['notes']
        print(uploaded_file.name)
        
    return render(request,'Semester/User-Notes/Notes.html')

def index(request):
    subjects = Subjects.objects.all().order_by('id')
    return render(request, 'Main-Site/index.html',{'subjects':subjects})

@login_required(login_url = 'login')
def maths1(request):
    return render(request, 'Semester/1st semester/Maths/1st_sem_math.html')
@login_required(login_url = 'login')
def tc(request):
    return render(request, 'Semester/1st semester/TC/1st_sem_tc.html')
@login_required(login_url = 'login')
def phy(request):
    return render(request, 'Semester/1st semester/Physics/1st_sem_phy.html')
@login_required(login_url = 'login')
def c(request):
    return render(request, 'Semester/1st semester/C/1st_sem_C.html')
@login_required(login_url = 'login')
def fit(request):
    return render(request, 'Semester/1st semester/FIT/1st_sem_fit.html')

