from django.urls import path

from api.views import auth, user

urlpatterns = [
    path('auth/send_sms_code/', auth.SendCodeView.as_view()),
    path('auth/login/', auth.LoginView.as_view()),
    path('auth/certification/', auth.CertificationView.as_view()),

    path('user/info/', user.UserInfoView.as_view()),
]
