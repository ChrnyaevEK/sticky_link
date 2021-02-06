from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

auth_urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name="django_authentication/login.html"
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name="website/website.html"
        ),
        name='logout'
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name="django_authentication/password_change.html"
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name="django_authentication/password_change_done.html"
        ),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="django_authentication/password_reset.html",
            email_template_name="django_authentication/password_reset_email.txt",
            subject_template_name="django_authentication/password_reset_subject.txt",
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="django_authentication/password_reset_done.html"
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="django_authentication/password_reset_confirm.html"
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="django_authentication/password_reset_complete.html"
        ),
        name='password_reset_complete'
    ),
]

urlpatterns = [
    path('', include('website.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include(auth_urlpatterns)),
    path('app/', include('application.urls')),
    path('admin/', admin.site.urls),
]
