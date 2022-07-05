from django.urls import path
from .modules.login import LoginView
from .modules.logout import LogoutView
from .modules.user import UserDetailView
from .modules.register import RegisterView
from .modules.activate import ActivateAPIView
from .modules.refresh import CookieRefreshView
from .modules.reset_password import ResetPasswordView
from .modules.forgot_password import ForgotPasswordView
from .modules.update_password import UpdatePasswordView
from .modules.auth_status import AuthenticationStatusView
from .modules.verify_mail_change import VerifyMailChangeView
from .modules.request_mail_change import RequestMailChangeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login-api'),
    path('logout/', LogoutView.as_view(), name='logout-api'),
    path('info/', UserDetailView.as_view(), name='user-api'),
    path('register/', RegisterView.as_view(), name='register-api'),
    path('activate/', ActivateAPIView.as_view(), name='activate-api'),
    path('refresh/', CookieRefreshView.as_view(), name='refresh-api'),
    path('verify/', AuthenticationStatusView.as_view(), name='verify-auth-api'),
    path('verify-mail/', VerifyMailChangeView.as_view(), name='verify-mail-api'),
    path('change-mail/', RequestMailChangeView.as_view(), name='change-mail-api'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password-api'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password-api'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password-api'),
]
