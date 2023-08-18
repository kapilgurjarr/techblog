from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.urls import reverse_lazy

from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from celery.result import AsyncResult

from accounts.models import UserProfile
from accounts.forms import UserRegisterForm,LoginAuthenticationForm
from accounts.token.account_activate_token import account_activation_token
from accounts.task import send_mail_task
from accounts.sendActivateMail import accountActivateMailSend
# from accounts.activate import activate

# Create your views here.

class UserRegistrationView(CreateView):
    form_class=UserRegisterForm
    template_name='registration.html'
    success_url=reverse_lazy('user-registration')

    def post(self,request):
        site = get_current_site(request) # for the domain

        form=UserRegisterForm(request.POST)
        if form.is_valid():
            # user_email = form.cleaned_data['email']
            user=form.save()
            accountActivateMailSend(user)
            # message = render_to_string('account/activate_account_mail.html', {
            #     'user': f"{user.first_name}{user.last_name}",
            #     'protocol': 'http',
            #     'domain': site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })  # filling the  activation mail template w/ all the variables 
            # send_mail_task.delay(message,user.email)
            messages.success(request,'Account is created successfully. Check your email and activate your account')
            return redirect(reverse_lazy('blog:index'))

        messages.error(request,'your detail is invlid please registration again')
        return redirect(reverse_lazy('user-registration'))
        


class ActivateAccountView(RedirectView):
    http_method_names=['get']
    pattern_name=reverse_lazy('user-registration')
    query_string = True
    
    def get_redirect_url(self, *args, **kwargs):
        return self.pattern_name


    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True  # now we're activating the user
            user.save()
            # login(request, user)  # log the user in
            messages.add_message(request, messages.INFO, 'Hi {0} your email is verify.'.format(request.user))
        else:
            messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')
            return HttpResponse('Account activation link is invalid.')

        return super().get(request, *args, **kwargs)
        


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    authentication_form = LoginAuthenticationForm
    
    
    def form_valid(self,form):
        email = form.cleaned_data['username']
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            messages.error(self.request,'User DoesNotExist')
            return HttpResponseRedirect(reverse_lazy('user-login'))
        if user.is_superuser:
            messages.error(self.request,'INVALID_CREDENTIALS')
            return HttpResponseRedirect(reverse_lazy('user-login'))
        if user.is_active:
            login(self.request,user)
            return HttpResponseRedirect(self.get_success_url())
        messages.error(self.request,'your account is not activate please check your email activate your account')
        return HttpResponseRedirect(reverse_lazy('user-login'))
        


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
    


class SettingView(LoginRequiredMixin, View):
    
    template_name = 'settings.html'

    def get(self, request):
        if not request.user.is_superuser:
            try:
                user_profile=UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                user_profile=None
            context={
                'UserInfo':User.objects.get(username=request.user),
                'user_profile':user_profile
            }

            return render(request, self.template_name, context)
        return redirect(reverse_lazy('user-login'))







class DeactivateUserAccount(LoginRequiredMixin, View):

    template_name = 'deactivate_account.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        account = User.objects.get(username=request.user)
        account.is_active=False
        account.save()
        return redirect(reverse_lazy('accounts:user-logout'))


class ActivateAccountMailSendView(View):

    template_name=''

    def get(self, request, *args, **kwargs):
        return render(request, template_name)
    
    def post(self, request, *args, **kwargs):
        email=request.POST['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,'you enter wrong email, please enter currect email')
            return redirect(reverse_lazy(''))
        accountActivateMailSend(user)
        messages.success(request,'Account activate mail send successfully. Check your email and activate your account')
        return redirect(reverse_lazy('accounts:login'))
    
class UserEmailUpdateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        email=request.POST['email']
        user=User.objects.get(email=email)
        if user.email==email:
            return redirect(reverse_lazy('accounts:user-setting'))
        user.email=email
        user.is_active=False
        user.save()
        accountActivateMailSend(user)
        messages.success(request,'Your email is update successfully. Check your mail and confirm your email')
        return redirect(reverse_lazy('accounts:login'))



class UserProfileUpdateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        bio=request.POST.get('bio')

        user=User.objects.get(username=request.user)
        user.first_name=fname
        user.last_name=lname

        if bio is not None:
            try:
                user_profile=UserProfile.objects.get(user=request.user)
                user_profile.bio=bio
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=request.user, bio=bio)
            return redirect(reverse_lazy('accounts:user-setting'))
