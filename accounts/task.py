from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings




@shared_task
def send_mail_task(message,user_email):
    str_message = strip_tags(message)
    msg = EmailMultiAlternatives(
                'Email Varification',
                str_message,
                settings.EMAIL_HOST_USER,
                [user_email],
                )
    msg.attach_alternative(message,'text/html')
    msg.send()
    return 'Send Mail'