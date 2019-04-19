from django.urls import path

from api.views.core import auth

urlpatterns = [
    path('auth/login/', auth.LoginView.as_view()),
]
