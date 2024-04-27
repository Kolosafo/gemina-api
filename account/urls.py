from django.urls import path
from django.views.generic import TemplateView
from . import views

from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'accounts'
urlpatterns = [
    path('register/',
         views.register, name="register"),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('resend_verification/',  views.SendVerificationLinkView.as_view(), name='resend-verification'),
    # path('change_password/', views.change_password, name="change_password"),
    # path('change_username/', views.change_username, name="change_username"),
    # path('verify_token/', views.verify_access_token, name="verify_access_token"),
    # path('forgot_password/', views.forgot_password, name="forgot_password"),
    # path('password_reset/', views.password_reset, name="password_reset"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
