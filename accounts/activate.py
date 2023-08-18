from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.token.account_activate_token import account_activation_token



@require_http_methods(["GET"])
def activate(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # now we're activating the user
        user.save()
        # login(request, user)  # log the user in
        messages.add_message(request, messages.INFO, 'Hi {0} your email is verify.'.format(request.user))
    else:
        messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')

    return redirect('/')