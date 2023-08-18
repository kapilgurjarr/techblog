from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts import views

app_name='accounts'

urlpatterns = [
    path('registration/',views.UserRegistrationView.as_view(),
        name='user-registration'),

    path('activate/<uidb64>/<token>/',views.ActivateAccountView.as_view(),
    name='email-activate'),

    path('login/',views.UserLoginView.as_view(),
    name='user-login'),

    path('logout/',views.LogoutView.as_view(),
    name='user-logout'),

    path('me/setting/',views.SettingView.as_view(),
    name='user-setting'),

    path('me/emailUpdate/',views.UserEmailUpdateView.as_view(),
    name='update-user-email'),

    path('me/profileUpdate/',views.UserProfileUpdateView.as_view(),
    name='update-user-profile'),

    path('deactivate_account/',views.DeactivateUserAccount.as_view(),
    name='deactivate-user-account'),
]
