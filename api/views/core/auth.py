from rest_framework import generics

from api.serializer.auth import LoginSerializer
from shared.common.response import *


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return response_400(serializer.errors)
        return response_200(None)

