from django.urls import path
from django.conf import settings
from kt_auth.pillars.views import PillarsView
from kt_auth.signin.views import AuthSigninView, TemporarySigninView, signout
from kt_auth.signup.views import AuthSignupView
from kt_auth.reset_password.views import AuthResetPasswordView
from kt_auth.new_password.views import AuthNewPasswordView

app_name = 'kt_auth'

urlpatterns = [
    path('signin', AuthSigninView.as_view(template_name = 'pages/auth/signin.html'), name='signin'),
    path('signup', AuthSignupView.as_view(template_name = 'pages/auth/signup.html'), name='signup'),
    path('reset-password', AuthResetPasswordView.as_view(template_name = 'pages/auth/reset-password.html'), name='reset-password'),
    path('new-password', AuthNewPasswordView.as_view(template_name = 'pages/auth/new-password.html'), name='new-password'),

    path('temporary/signin', TemporarySigninView.as_view(), name="temporary-signin"),
    path('signout', signout, name="signout"),

    path('pillars', PillarsView.as_view(), name="pillars"),
]