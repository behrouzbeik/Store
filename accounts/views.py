from django.shortcuts import render,redirect,reverse
from .forms import *
from .models import *
from order.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
import ghasedak
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy





class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

email_generator = EmailToken()

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'],email=data['email'],first_name=data['first_name'],
                                     last_name=data['last_name'],password=data['password_2'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active',kwargs={'uidb64':uidb64,'token':email_generator.make_token(user)})
            links = 'http://' + domain + url
            email = EmailMessage(
                'active user',
                links,
                'test<paneldjango@gmail.com>',
                [data['email']]
            )
            email.send(fail_silently=False)
            messages.warning(request,'karbar mohtaram lotfan jahat faalsazi b email khod morajee namei','warning')
            return redirect('home:home')

    else:
        form = UserRegisterForm()


    context = { 'form':form }
    return render(request,'accounts/register.html',context)

def user_login(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            remember = data['remember']
            try:
                user = authenticate (request,username=User.objects.get(email=data['user']),password=data['password'])
            except:
                user = authenticate(request,username=data['user'],password=data['password'])
            if user is not None:
                login(request,user)
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(10000)
                messages.success(request,'welcome to site','primary')
                return redirect('home:home')
            else:
                messages.success(request,'user or password wrong ','danger')

    else:
        form = UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})


def user_logout(request):
    logout(request)
    messages.success(request,'با موفقیت انجام شد','warning')
    return redirect('home:home')

class RegisterEmail(View):
    def get(self,request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


@login_required(login_url='accunts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request,'accounts/profile.html',{'profile':profile})



@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'update successfully','success')
            return redirect('accounts:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_form':user_form,'profile_form':profile_form}
    return render(request,'accounts/update.html',context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'password change','success')
            return redirect('accounts:profile')
        else:
            messages.success(request,'paswword fail','danger')
            return redirect('accounts:change')
    else :
        form = PasswordChangeForm(request.user)

    return render(request,'accounts/change.html',{'form':form})



def phone(request):
    if request.method=='POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            global random_code,phone
            data = form.cleaned_data
            phone = f"0{data['phone']}"
            random_code = randint(100,1000)
            sms = ghasedak.Ghasedak("0c2eba3047039348177a1565837633b259a2bb076dc12bbb414bcb61004f87ab")
            sms.send({'message': random_code, 'receptor': phone, 'linenumber': "10008566"})
            return redirect('accounts:verify')

    else:
        form = PhoneForm()

    return render(request,'accounts/phone.html',{'form':form})



def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request,user)
                messages.success(request,'hi user')
                return redirect('home:home')
            else:
                messages.error(request,'code fail')
    else:
        form=CodeForm()
    return render(request,'accounts/code.html',{'form':form})


def favourite(request):
    product = request.user.fa_user.all()
    return render(request,'accounts/favourite.html',{'product':product})


def product_view(request):
    # product =Product.objects.filter(view=request.user.id)
    views = Views.objects.filter(ip=request.META.get('REMOTE_ADDR')).order_by('-create')[:2]
    return render(request,'accounts/view.html',{'views':views})



class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'

class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'

class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:compelet')

class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/compelete.html'


def history(request):
    data = ItemOrder.objects.filter(user_id=request.user.id)
    return render(request,'accounts/history.html',{'data':data})

