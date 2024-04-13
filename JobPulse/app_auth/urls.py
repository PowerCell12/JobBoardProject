from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from JobPulse.app_auth.forms import CustomLoginForm
from JobPulse.app_auth.views import SignUpView, LogOutView, SignUpUser, SignUpRecruiter, profile_description, \
    profile_edit, profile_delete

urlpatterns = [
    path('login/',  LoginView.as_view(template_name='app_auth/login_profile.html', authentication_form=CustomLoginForm), name='login-profile'),
    path('signup/', SignUpView, name='signup'),
    path('signup/user/', SignUpUser, name='signup-user'),
    path('sigup/recruiter/', SignUpRecruiter, name='signup-recruiter'),
    path('<int:pk>/logout/', LogOutView, name='logout-profile'),
    path('<int:pk>/description/', profile_description, name='description-profile'),
    path('<int:pk>/edit/', profile_edit, name='edit-profile'),
    path('<int:pk>/delete/', profile_delete.as_view(), name='delete-profile' ),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

