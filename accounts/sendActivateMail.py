from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.token.account_activate_token import account_activation_token
from accounts.task import send_mail_task



def accountActivateMailSend(user):
    site = get_current_site(request)
    message = render_to_string('account/activate_account_mail.html', {
                'user': f"{user.first_name}{user.last_name}",
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })  # filling the  activation mail template w/ all the variables 
    send_mail_task.delay(message,user.email)