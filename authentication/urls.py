from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

from .forms import MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path("login", views.log_in_user, name='login'),
    path("signup", views.RegisterView.as_view(), name='signup'),
    path("successfully-completed", views.successfully_completed, name='successfully_completed'),
    path('password-change', auth_view.PasswordChangeView.as_view(
        template_name='authentication/change_password.html', form_class=MyPasswordChangeForm,
        success_url='passwordchangedone'), name='password_change'),

    path('passwordchangedone', auth_view.PasswordChangeDoneView.as_view(
        template_name='authentication/successfully_completed.html'), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='authentication/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'
    ),

    path('password-reset/done', auth_view.PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html', form_class=MySetPasswordForm),
         name='password_reset_confirm'),

    path('password-reset-complete', auth_view.PasswordResetCompleteView.as_view(
        template_name='authentication/successfully_completed.html'), name='password_reset_complete'),

    path("logout", views.logout_user, name='logout'),
]
