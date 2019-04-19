from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from api.serializer.auth import LoginSerializer


class TokenView(generics.ListCreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
