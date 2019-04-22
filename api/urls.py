from django.urls import path

from api.views.core import auth

urlpatterns = [
    path('auth/send_sms_code/', auth.SendCodeView.as_view()),
    path('auth/login/', auth.LoginView.as_view()),
]
