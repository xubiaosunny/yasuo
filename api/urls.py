from django.urls import path

from api.views import auth, user

urlpatterns = [
    path('auth/send_sms_code/', auth.SendCodeView.as_view()),
    path('auth/token/', auth.TokenView.as_view()),
    path('auth/certification/', auth.CertificationView.as_view()),

    path('user/info/', user.UserInfoView.as_view()),
    path('user/follow/', user.UserFollowView.as_view()),
    path('user/cities/', user.UserCityView.as_view()),
    path('user/grades/', user.UserGradeView.as_view()),
]
